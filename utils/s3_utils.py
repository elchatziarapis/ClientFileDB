import boto3
import uuid
import configparser
from botocore.exceptions import NoCredentialsError, ClientError
from datetime import datetime, timezone
from logger import Logger

# Initialize logger
logger = Logger.get_logger()

# Read configuration
config = configparser.ConfigParser()
config.read('config/config.ini')
logger.info("Configuration file read successfully.")

# AWS configuration
AWS_ACCESS_KEY_ID = config['AWSBucketS3']['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = config['AWSBucketS3']['aws_secret_access_key']
AWS_REGION_NAME = config['AWSBucketS3']['aws_region_name']
S3_BUCKET_NAME = config['AWSBucketS3']['s3_bucket_name']

class S3Utils:
    """
    A utility class for handling S3 operations such as uploading, downloading, deleting files,
    generating pre-signed URLs, and checking S3 connection.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    )

    @staticmethod
    def generate_s3_key(file_name):
        """
        Generate a unique S3 key for the file.
        
        Args:
            file_name (str): The name of the file.
        
        Returns:
            str: A unique S3 key for the file.
        """
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4())
        return f"{timestamp}_{unique_id}_{file_name}"
    
    @staticmethod
    def upload_file_to_s3(file_content, file_name, file_s3_key):
        """
        Upload a file to S3.
        
        Args:
            file_content (bytes): The content of the file.
            file_name (str): The name of the file.
            file_s3_key (str): The S3 key for the file.
        
        Returns:
            str: The S3 key of the uploaded file if successful, None otherwise.
        """
        try:
            logger.info(f"Starting upload of file: {file_name} with key: {file_s3_key}")
            S3Utils.s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=file_s3_key, Body=file_content)
            logger.info(f"File uploaded successfully: {file_name} with key: {file_s3_key}")
            return file_s3_key
        except NoCredentialsError:
            logger.error("Credentials not available")
            return None
        except Exception as e:
            logger.error(f"Error uploading file: {file_name}, Error: {str(e)}")
            return None

    @staticmethod
    def download_file_from_s3(file_name):
        """
        Download a file from S3.
        
        Args:
            file_name (str): The S3 key of the file to be downloaded.
        
        Returns:
            bytes: The content of the file if successful, None otherwise.
        """
        try:
            response = S3Utils.s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_name)
            return response['Body'].read()
        except (NoCredentialsError, ClientError) as e:
            logger.error(f"Error downloading file: {str(e)}")
            return None

    @staticmethod
    def delete_file_from_s3(file_name):
        """
        Delete a file from S3.
        
        Args:
            file_name (str): The S3 key of the file to be deleted.
        
        Returns:
            bool: True if the file was successfully deleted, False otherwise.
        """
        try:
            logger.info(f"Starting deletion of file: {file_name}")
            response = S3Utils.s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=file_name)
            logger.info(f"Delete response from S3: {response}")

            # Check if the file was actually deleted
            if 'DeleteMarker' in response and response['DeleteMarker']:
                logger.info(f"File deleted successfully: {file_name}")
                return True
            else:
                logger.warning(f"File may not have been deleted: {file_name}")
                return False
        except NoCredentialsError:
            logger.error("Credentials not available")
            return False
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                logger.info(f"File not found in S3: {file_name}")
                return True
            else:
                logger.error(f"Client error deleting file: {file_name}, Error: {str(e)}")
                return False
        except Exception as e:
            logger.error(f"Error deleting file: {file_name}, Error: {str(e)}")
            return False

    @staticmethod
    def generate_presigned_url(s3_key, expiration=3600):
        """
        Generate a pre-signed URL for an S3 object.
        
        Args:
            s3_key (str): The S3 key of the object.
            expiration (int): Time in seconds for the pre-signed URL to remain valid.
        
        Returns:
            str: The pre-signed URL if successful, None otherwise.
        """
        try:
            url = S3Utils.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_BUCKET_NAME, 'Key': s3_key},
                ExpiresIn=expiration
            )
            logger.info(f"Presigned URL generated: {url}")
            return url
        except Exception as e:
            logger.error(f"Error generating presigned URL: {str(e)}")
            return None

    @staticmethod
    def check_s3_connection():
        """
        Check the connection to the S3 bucket.
        
        Returns:
            bool: True if connected successfully, False otherwise.
        """
        try:
            # Perform a simple operation to check connection, like listing objects in the bucket
            S3Utils.s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)
            logger.info("Connected to S3 successfully.")
            return True
        except (NoCredentialsError, ClientError) as e:
            logger.error(f"Error connecting to S3: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error connecting to S3: {str(e)}")
            return False
