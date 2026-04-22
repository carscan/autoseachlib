"""
Tests for S3 utilities.
"""

import os
import pytest
from moto import mock_aws
import boto3
from autoseachlib.s3 import download_image


@mock_aws
def test_download_image_success(tmp_path):
    # Setup mock S3
    s3 = boto3.client("s3", region_name="us-east-1")
    bucket = "test-bucket"
    key = "test-image.jpg"
    content = b"fake image content"
    s3.create_bucket(Bucket=bucket)
    s3.put_object(Bucket=bucket, Key=key, Body=content)
    
    # Local path to save
    local_file = tmp_path / "downloaded.jpg"
    
    # Run download
    result = download_image(
        bucket=bucket,
        key=key,
        local_path=str(local_file),
        access_key="fake_key",
        secret_key="fake_secret"
    )
    
    assert result is True
    assert local_file.exists()
    assert local_file.read_bytes() == content


@mock_aws
def test_download_image_missing_file(tmp_path):
    # Setup mock S3
    s3 = boto3.client("s3", region_name="us-east-1")
    bucket = "test-bucket"
    s3.create_bucket(Bucket=bucket)
    
    # Local path to save
    local_file = tmp_path / "downloaded.jpg"
    
    # Run download for non-existent key
    result = download_image(
        bucket=bucket,
        key="missing.jpg",
        local_path=str(local_file)
    )
    
    assert result is False
    assert not local_file.exists()
