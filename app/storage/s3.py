import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
from app.utils.logger import logger

class S3Storage:
    def __init__(self, bucket_name, access_key, secret_key, region):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        
    def upload_file(self, local_path):
     """Uploads a file to S3 and returns the S3 URL or success status."""
     file_name = os.path.basename(local_path)
     try:
        logger.info(f"Uploading {file_name} to S3 bucket: {self.bucket_name}")
        self.s3_client.upload_file(local_path, self.bucket_name, file_name)
        s3_url = f"s3://{self.bucket_name}/{file_name}"
        return True, s3_url
     except FileNotFoundError:
        logger.error(f"File not found: {local_path}")
        raise
     except NoCredentialsError:
        logger.error("AWS credentials not found")
        raise
     except ClientError as e:
        logger.error(f"Error occurred while uploading file to S3: {e}")
        raise