import logging
import os
import boto3


class S3BucketConfig:
    def __init__(self, bucket_name, aws_access_key_id, aws_secret_access_key, aws_region):
        self.bucket_name = bucket_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.bucket_name = bucket_name
        self.aws_region = aws_region


def upload_file_to_s3_bucket(file_path: str, bucket_name: str, aws_access_key_id: str, aws_secret_access_key: str,
                             object_name: str = None):
    if object_name is None:
        object_name = file_path
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        s3_client.upload_file(file_path, bucket_name, object_name, )
        logging.info(f"File '{file_path}' uploaded to bucket '{bucket_name}' as '{object_name}'.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def upload_directory_to_s3_bucket(local_directory: str, bucket_name: str, aws_access_key_id: str,
                                  aws_secret_access_key: str, s3_directory: str = ''):
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_directory)
            s3_file_path = os.path.join(s3_directory, relative_path).replace("\\", "/")
            try:
                upload_file_to_s3_bucket(file_path=local_file_path, bucket_name=bucket_name, object_name=s3_file_path,
                                         aws_access_key_id=aws_access_key_id,
                                         aws_secret_access_key=aws_secret_access_key)
                logging.info(f"File '{local_file_path}' uploaded to bucket '{bucket_name}' as '{s3_file_path}'.")
            except Exception as e:
                logging.error(f"An error occurred: {e}")
