"""
S3 Utilities for AutoSeachLib.
"""

import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError


def get_s3_client(
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    region_name: Optional[str] = None,
):
    """
    Create a boto3 S3 client.
    
    If access_key and secret_key are provided, they will be used.
    Otherwise, the client will use the default session (IAM roles, environment variables, or ~/.aws/credentials).
    """
    session_kwargs = {}
    if access_key and secret_key:
        session_kwargs["aws_access_key_id"] = access_key
        session_kwargs["aws_secret_access_key"] = secret_key
    
    if region_name:
        session_kwargs["region_name"] = region_name
        
    return boto3.client("s3", **session_kwargs)


def download_image(
    bucket: str,
    key: str,
    local_path: str,
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> bool:
    """
    Download an image (or any file) from S3.
    
    Args:
        bucket: The name of the S3 bucket.
        key: The key (path) of the file in S3.
        local_path: The local path where the file should be saved.
        access_key: Optional AWS access key.
        secret_key: Optional AWS secret key.
        region_name: Optional AWS region.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    client = get_s3_client(access_key, secret_key, region_name)
    
    # Ensure local directory exists
    os.makedirs(os.path.dirname(os.path.abspath(local_path)), exist_ok=True)
    
    try:
        print(f"Downloading s3://{bucket}/{key} to {local_path}...")
        client.download_file(bucket, key, local_path)
        print("Download successful.")
        return True
    except ClientError as e:
        print(f"Error downloading from S3: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
