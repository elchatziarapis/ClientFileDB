from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.file import File
from utils.s3_utils import S3Utils
from database import Database
from datetime import datetime, timezone
from logger import Logger
import os

logger = Logger.get_logger()

class FileService:
    def __init__(self, db: Database):
        """
        Initialize the FileService with a Database instance.

        Args:
            db (Database): An instance of the Database class.
        """
        self.db = db

    def create_file(self, name: str, folder_id: int, file_content: bytes) -> File:
        """
        Create a new file with the given name and content in the specified folder.

        Args:
            name (str): The name of the file.
            folder_id (int): The ID of the folder where the file will be created.
            file_content (bytes): The content of the file.

        Returns:
            File: The created File object.

        Raises:
            IntegrityError: If a database integrity error occurs.
            Exception: If any other error occurs during file creation.
        """
        s3_key = S3Utils.generate_s3_key(name)
        size = len(file_content)

        with self.db.get_db_session() as session:
            try:
                file = File(
                    file_name=name,
                    file_size=size,
                    folder_id=folder_id,
                    file_created_date=datetime.now(timezone.utc),
                    file_s3_key=s3_key
                )
                session.add(file)
                session.commit()
                session.refresh(file)
                logger.info(f"File record created in the database: {name}, File ID: {file.file_id}")
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Database error occurred: {str(e)}", exc_info=True)
                raise
            except Exception as e:
                session.rollback()
                logger.error(f"Error in create_file: {e}", exc_info=True)
                raise

        if not S3Utils.upload_file_to_s3(file_content, name, s3_key):
            logger.error(f"Failed to upload file to S3: {name}")
            with self.db.get_db_session() as session:
                try:
                    session.delete(file)
                    session.commit()
                    logger.info(f"Cleaned up database record for file ID: {file.file_id} after failed S3 upload")
                except Exception as cleanup_exception:
                    logger.error(f"Failed to clean up database record for file ID: {file.file_id} after failed S3 upload: {cleanup_exception}", exc_info=True)
            raise Exception("File upload to S3 failed")

        return file

    def get_file(self, file_id: int) -> File:
        """
        Retrieve details of a file by its ID.

        Args:
            file_id (int): The ID of the file.

        Returns:
            File: The File object containing file details.

        Raises:
            Exception: If the file is not found in the database or any other error occurs during retrieval.
        """
        with self.db.get_db_session() as session:
            try:
                file = session.query(File).filter_by(file_id=file_id).first()
                if not file:
                    logger.error(f"File not found: File ID: {file_id}")
                    raise Exception("File not found in the database")
                return file
            except Exception as e:
                logger.error(f"Error in get_file: {e}", exc_info=True)
                raise


    def delete_file(self, file_id: int) -> File:
        """
        Delete a file by its ID from the database and S3.

        Args:
            file_id (int): The ID of the file to be deleted.

        Raises:
            IntegrityError: If a database integrity error occurs.
            Exception: If any other error occurs during file deletion.
        """
        file_s3_key = None

        with self.db.get_db_session() as session:
            try:
                file = session.query(File).filter_by(file_id=file_id).first()
                if not file:
                    logger.error(f"File not found in the database: File ID: {file_id}")
                    raise Exception(f"File not found in the database: File ID: {file_id}")

                file_s3_key = file.file_s3_key

                s3_deletion_success = True
                if file_s3_key:
                    s3_deletion_success = S3Utils.delete_file_from_s3(file_s3_key)
                    if not s3_deletion_success:
                        logger.warning(f"File not found in S3: {file_s3_key}")
                
                session.delete(file)
                session.commit()
                logger.info(f"File deleted successfully from database: File ID: {file_id}")
                return file
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Database error occurred: {str(e)}", exc_info=True)
                raise
            except Exception as e:
                session.rollback()
                logger.error(f"Error in delete_file: {e}", exc_info=True)
                raise


    # TODO
    def create_file_from_local(self, local_file_path: str, folder_id: int) -> File:
        pass

    # TODO
    def download_file(self, file_id: int, local_path: str) -> str:
        pass
    
