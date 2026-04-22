"""
Dataset processing utilities for AutoSeachLib.
"""

import os
import json
import ast
import pandas as pd
from PIL import Image
from tqdm import tqdm
from autoseachlib.s3 import download_image


class DatasetBuilder:
    """
    Builds model training datapacks from a CSV dataset.
    Downloads images from S3 and formats annotations for computer vision
    tasks (Object Detection, Segmentation via COCO format) and VLM tasks.
    """

    def __init__(self, output_dir: str):
        """
        Initialize the DatasetBuilder.

        Args:
            output_dir (str): The root directory where the datapack will be created.
        """
        self.output_dir = output_dir
        self.images_dir = os.path.join(output_dir, "images")
        self.annotations_dir = os.path.join(output_dir, "annotations")
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.annotations_dir, exist_ok=True)

    def process_csv(self, csv_path: str):
        """
        Process the CSV file, download images, and generate annotation formats.

        Args:
            csv_path (str): Path to the dataset CSV file.
            
        Returns:
            tuple: Paths to the generated COCO JSON and VLM JSONL files.
        """
        print(f"Reading CSV from {csv_path}...")
        df = pd.read_csv(csv_path)

        coco_format = {
            "images": [],
            "annotations": [],
            "categories": []
        }

        vlm_format = []

        # Categories
        category_map = {}
        category_id_counter = 1

        # Group by image to handle multiple annotations per image
        if 'image_name' not in df.columns:
            raise ValueError("CSV must contain an 'image_name' column.")
            
        grouped = df.groupby('image_name')

        image_id_counter = 1
        annotation_id_counter = 1

        for image_name, group in tqdm(grouped, desc="Processing Images"):
            first_row = group.iloc[0]
            s3_path = first_row.get('s3_path')
            # The first 'name' column is typically the bucket name
            bucket = first_row.get('name')

            if not s3_path or not bucket:
                print(f"Skipping {image_name}: Missing s3_path or bucket name.")
                continue

            local_image_path = os.path.join(self.images_dir, image_name)

            # Download image if it does not exist locally
            if not os.path.exists(local_image_path):
                # Suppress the print statements from download_image to avoid flooding tqdm
                success = download_image(bucket, s3_path, local_image_path)
                if not success:
                    print(f"Failed to download {image_name} from S3.")
                    continue

            # Get image dimensions required by COCO
            try:
                with Image.open(local_image_path) as img:
                    width, height = img.size
            except Exception as e:
                print(f"Error reading image {local_image_path}: {e}")
                continue

            image_info = {
                "id": image_id_counter,
                "file_name": image_name,
                "width": width,
                "height": height
            }
            coco_format["images"].append(image_info)

            descriptions = []

            for _, row in group.iterrows():
                # pandas handles duplicate column names by appending .1, .2
                category_name = row.get('name.1', 'unknown')
                sub_type = row.get('sub_type')

                # Use sub_type as category name if available, else fallback to name.1
                cat_label = sub_type if pd.notna(sub_type) else category_name

                if cat_label not in category_map:
                    category_map[cat_label] = category_id_counter
                    coco_format["categories"].append({
                        "id": category_id_counter,
                        "name": cat_label,
                        "supercategory": category_name
                    })
                    category_id_counter += 1

                cat_id = category_map[cat_label]

                # Parse bounding box: [xmin, ymin, xmax, ymax] -> COCO [xmin, ymin, width, height]
                bbox_str = row.get('bounding_box')
                bbox = []
                area = 0
                if pd.notna(bbox_str):
                    try:
                        bbox_coords = ast.literal_eval(bbox_str)
                        if len(bbox_coords) == 4:
                            x_min, y_min, x_max, y_max = bbox_coords
                            w = x_max - x_min
                            h = y_max - y_min
                            bbox = [x_min, y_min, w, h]
                            area = w * h
                    except (ValueError, SyntaxError):
                        pass

                # Parse polygon
                polygon_str = row.get('polygon')
                segmentation = []
                if pd.notna(polygon_str):
                    try:
                        segmentation = ast.literal_eval(polygon_str)
                    except (ValueError, SyntaxError):
                        pass

                annotation_info = {
                    "id": annotation_id_counter,
                    "image_id": image_id_counter,
                    "category_id": cat_id,
                    "bbox": bbox,
                    "segmentation": segmentation,
                    "area": area,
                    "iscrowd": 0
                }
                coco_format["annotations"].append(annotation_info)
                annotation_id_counter += 1

                desc = row.get('description')
                if pd.notna(desc) and desc not in descriptions:
                    descriptions.append(desc)

            # Add to VLM format if descriptions exist
            if descriptions:
                vlm_format.append({
                    "image": f"images/{image_name}",
                    "text": " ".join(descriptions)
                })

            image_id_counter += 1

        # Save COCO format JSON
        coco_path = os.path.join(self.annotations_dir, "coco_annotations.json")
        with open(coco_path, 'w') as f:
            json.dump(coco_format, f, indent=2)

        # Save VLM format JSONL
        vlm_path = os.path.join(self.annotations_dir, "vlm_annotations.jsonl")
        with open(vlm_path, 'w') as f:
            for item in vlm_format:
                f.write(json.dumps(item) + '\n')

        print(f"\nDatapack successfully created in: {self.output_dir}")
        print(f"- COCO annotations (Detection/Segmentation): {coco_path}")
        print(f"- VLM annotations (Vision-Language): {vlm_path}")
        
        return coco_path, vlm_path

