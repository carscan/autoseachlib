import os
import json
from unittest.mock import patch, MagicMock
from autoseachlib.dataset import DatasetBuilder
import pandas as pd

def test_dataset_builder_init(tmp_path):
    builder = DatasetBuilder(str(tmp_path), draw_review="both")
    assert builder.draw_review == "both"
    assert os.path.exists(os.path.join(tmp_path, "review_images"))

@patch("autoseachlib.dataset.download_image")
@patch("autoseachlib.dataset.Image.open")
def test_process_csv_with_review(mock_image_open, mock_download, tmp_path):
    # Mock image size to return 100x100
    mock_img = MagicMock()
    mock_img.size = (100, 100)
    mock_img.convert.return_value = mock_img
    mock_image_open.return_value.__enter__.return_value = mock_img
    
    mock_download.return_value = True

    csv_path = tmp_path / "test.csv"
    df = pd.DataFrame({
        "id": [1],
        "name": ["test-bucket"],
        "s3_path": ["path/to/test.jpg"],
        "image_name": ["test.jpg"],
        "polygon": ["[[0, 0, 10, 0, 10, 10, 0, 10]]"],
        "bounding_box": ["[0, 0, 10, 10]"],
        "sub_type": ["broken"],
        "description": ["Test desc"]
    })
    df.to_csv(csv_path, index=False)

    builder = DatasetBuilder(str(tmp_path), csv_path=str(csv_path), draw_review="both")
    coco_path, vlm_path = builder.process_csv()

    assert os.path.exists(coco_path)
    assert os.path.exists(vlm_path)

    # Check coco format
    with open(coco_path) as f:
        coco_data = json.load(f)
        assert len(coco_data["images"]) == 1
        assert len(coco_data["annotations"]) == 1
        # bbox [0,0,10,10] width=10, height=10
        assert coco_data["annotations"][0]["bbox"] == [0, 0, 10, 10]

    # Check that draw calls were made (since we mocked the image and ImageDraw is called on it)
    mock_img.convert.assert_called()
    mock_img.save.assert_called_with(os.path.join(tmp_path, "review_images", "test.jpg"))
