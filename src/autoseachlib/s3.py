"""
S3 Utilities for AutoSeachLib.
"""

import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


def get_s3_client(
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    region_name: Optional[str] = None,
):
    """
    Create a boto3 S3 client.
    
    Order of precedence for credentials:
    1. Explicitly passed arguments (access_key, secret_key).
    2. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).
    3. IAM Role / Default AWS credential chain.
    """
    session_kwargs = {}
    
    # Use provided keys or fall back to environment variables explicitly
    # (Boto3 does this automatically, but we can be explicit here)
    aws_access_key = access_key or os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = secret_key or os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")

    if aws_access_key and aws_secret_key:
        session_kwargs["aws_access_key_id"] = aws_access_key
        session_kwargs["aws_secret_access_key"] = aws_secret_key
    
    if aws_region:
        session_kwargs["region_name"] = aws_region
        
    return boto3.client("s3", **session_kwargs)


from tqdm import tqdm

def download_image(
    bucket: str,
    key: str,
    local_path: str,
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    region_name: Optional[str] = None,
    show_progress: bool = True,
) -> bool:
    """
    Download an image (or any file) from S3.
    
    Args:
        bucket: The name of the S3 bucket.
        key: The key (path) of the file in S3.
        local_path: The local path where the file should be saved.
        access_key: Optional AWS access key (overrides environment).
        secret_key: Optional AWS secret key (overrides environment).
        region_name: Optional AWS region (overrides environment).
        show_progress: Whether to show a download progress bar.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    client = get_s3_client(access_key, secret_key, region_name)
    
    # Ensure local directory exists
    os.makedirs(os.path.dirname(os.path.abspath(local_path)), exist_ok=True)
    
    try:
        if show_progress:
            try:
                meta = client.head_object(Bucket=bucket, Key=key)
                file_size = meta.get('ContentLength', 0)
            except ClientError:
                file_size = 0
                
            print(f"Downloading s3://{bucket}/{key} to {local_path}...")
            filename = key.split('/')[-1]
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=filename) as pbar:
                def progress_callback(bytes_amount):
                    pbar.update(bytes_amount)
                client.download_file(bucket, key, local_path, Callback=progress_callback)
            print("Download successful.")
        else:
            client.download_file(bucket, key, local_path)
            
        return True
    except ClientError as e:
        if show_progress: print(f"Error downloading from S3: {e}")
        return False
    except Exception as e:
        if show_progress: print(f"An unexpected error occurred: {e}")
        return False
