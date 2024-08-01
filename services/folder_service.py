from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from models.folder import Folder
from database import Database
from utils.s3_utils import S3Utils
from logger import Logger
from typing import List , Dict


logger = Logger.get_logger()

class FolderService:
    def __init__(self, db: Database):
        self.db = db

    def create_folder(self, name: str, parent_id: int = None) -> Folder:
        """
        Create a new folder in the database.

        Args:
            name (str): The name of the folder.
            parent_id (int, optional): The ID of the parent folder. Defaults to None.

        Returns:
            Folder: The created Folder object.

        Raises:
            Exception: If an error occurs during folder creation.
        """
        with self.db.get_db_session() as session:
            try:
                if parent_id == 0:
                    parent_id = None

                folder = Folder(folder_name=name, folder_parent_id=parent_id)
                session.add(folder)
                session.commit()
                session.refresh(folder)
                logger.info(f"Folder created successfully: {name}, Folder ID: {folder.folder_id}")
                return folder
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Database error occurred: {str(e)}", exc_info=True)
                raise Exception("Database integrity error occurred. Please check the logs for details.") from e
            except Exception as e:
                session.rollback()
                logger.error(f"Error in create_folder: {e}", exc_info=True)
                raise Exception("An error occurred while creating the folder. Please check the logs for details.") from e

    def get_folder(self, folder_id: int) -> Folder:
        """
        Retrieve a folder and its contents from the database.

        Args:
            folder_id (int): The ID of the folder to retrieve.

        Returns:
            Folder: The retrieved Folder object.

        Raises:
            Exception: If the folder is not found or another error occurs.
        """
        with self.db.get_db_session() as session:
            try:
                folder = session.query(Folder).options(joinedload(Folder.children), joinedload(Folder.files)).filter_by(folder_id=folder_id).first()
                if not folder:
                    logger.error(f"Folder not found: Folder ID: {folder_id}")
                    raise Exception("Folder not found in the database")
                return folder
            except Exception as e:
                logger.error(f"Error in get_folder: {e}", exc_info=True)
                raise Exception("An error occurred while retrieving the folder. Please check the logs for details.") from e

    def move_folder(self, folder_id: int, new_parent_id: int) -> Folder:
        """
        Move a folder to a new parent folder.

        Args:
            folder_id (int): The ID of the folder to move.
            new_parent_id (int): The ID of the new parent folder.

        Returns:
            Folder: The moved Folder object.

        Raises:
            Exception: If the folder is not found or another error occurs.
        """
        with self.db.get_db_session() as session:
            try:
                folder = session.query(Folder).filter_by(folder_id=folder_id).first()
                if not folder:
                    logger.error(f"Folder not found: Folder ID: {folder_id}")
                    raise Exception("Folder not found in the database")

                folder.folder_parent_id = new_parent_id
                session.commit()
                session.refresh(folder)
                logger.info(f"Folder moved successfully: Folder ID: {folder_id} to Parent ID: {new_parent_id}")
                return folder
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Database error occurred: {str(e)}", exc_info=True)
                raise Exception("Database integrity error occurred. Please check the logs for details.") from e
            except Exception as e:
                session.rollback()
                logger.error(f"Error in move_folder: {e}", exc_info=True)
                raise Exception("An error occurred while moving the folder. Please check the logs for details.") from e

    def delete_folder(self, folder_id: int) -> List[dict]:
        """
        Delete a folder and all its subfolders and files, returning a list of deleted items.

        Args:
            folder_id (int): The ID of the folder to delete.

        Returns:
            List[Dict]: A list of dictionaries representing the deleted folders and files.

        Raises:
            Exception: If the folder is not found or another error occurs.
        """
        deleted_items = []

        with self.db.get_db_session() as session:
            try:
                folder = session.query(Folder).options(joinedload(Folder.files)).filter_by(folder_id=folder_id).first()
                if not folder:
                    logger.error(f"Folder not found: Folder ID: {folder_id}")
                    raise Exception("Folder not found in the database")

                self._delete_folder_recursive(session, folder, deleted_items)

                session.commit()
                logger.info(f"Folder and all subfolders/files deleted successfully: Folder ID: {folder_id}")
                return deleted_items
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Database error occurred: {str(e)}", exc_info=True)
                raise Exception("Database integrity error occurred. Please check the logs for details.") from e
            except Exception as e:
                session.rollback()
                logger.error(f"Error in delete_folder: {e}", exc_info=True)
                raise Exception("An error occurred while deleting the folder. Please check the logs for details.") from e

    def _delete_folder_recursive(self, session: Session, folder: Folder, deleted_items: list):
        """
        Recursively delete a folder and its subfolders and files.

        Args:
            session (Session): The current database session.
            folder (Folder): The folder to delete.
            deleted_items (list): The list to store information about deleted items.
        """
        for file in folder.files:
            S3Utils.delete_file_from_s3(file.file_s3_key)
            session.delete(file)
            logger.info(f"Deleted file from S3 and database: File ID: {file.file_id}, S3 Key: {file.file_s3_key}")
            deleted_items.append({'type': 'file', 'id': file.file_id, 'name': file.file_name, 's3_key': file.file_s3_key})

        children = session.query(Folder).filter_by(folder_parent_id=folder.folder_id).all()
        for subfolder in children:
            self._delete_folder_recursive(session, subfolder, deleted_items)

        session.delete(folder)
        logger.info(f"Deleted folder from database: Folder ID: {folder.folder_id}")
        deleted_items.append({'type': 'folder', 'id': folder.folder_id, 'name': folder.folder_name})

    def list_files_and_subfolders(self, folder_id: int) -> Dict:
        """
        List all files and subfolders within a specified folder.

        Args:
            folder_id (int): The ID of the folder to list contents for.

        Returns:
            Dict: A dictionary containing the folder details, including its files and subfolders.

        Raises:
            Exception: If the folder is not found or another error occurs.
        """
        with self.db.get_db_session() as session:
            try:
                folder = session.query(Folder).options(joinedload(Folder.children), joinedload(Folder.files)).filter_by(folder_id=folder_id).first()
                if not folder:
                    logger.error(f"Folder not found: Folder ID: {folder_id}")
                    raise Exception("Folder not found in the database")

                # Recursive function to fetch all subfolders and files
                def get_subfolders_and_files(folder):
                    result = {
                        'Folder ID': folder.folder_id,
                        'Folder Name': folder.folder_name,
                        'Files': [{'File ID': file.file_id, 'File Name': file.file_name, 'File Size': file.file_size} for file in folder.files],
                        'Subfolders': []
                    }

                    for child in folder.children:
                        result['Subfolders'].append(get_subfolders_and_files(child))

                    return result

                output = get_subfolders_and_files(folder)
                logger.info(f"Listed files and subfolders for folder ID: {folder_id}")
                return output
            except Exception as e:
                logger.error(f"Error in list_files_and_subfolders: {e}", exc_info=True)
                print("Something went wrong while listing files and subfolders. Please check the log file for details.")
                raise

    def calculate_folder_size(self, folder_id: int) -> int:
        with self.db.get_db_session() as session:
            try:
                folder = session.query(Folder).options(joinedload(Folder.files)).filter_by(folder_id=folder_id).first()
                if not folder:
                    logger.error(f"Folder not found: Folder ID: {folder_id}")
                    raise Exception("Folder not found in the database")

                total_size = sum(file.file_size for file in folder.files)
                
                # Fetch and iterate over children explicitly
                children = session.query(Folder).filter_by(folder_parent_id=folder_id).all()
                for child in children:
                    total_size += self.calculate_folder_size(child.folder_id)
                    
                logger.info(f"Calculated size for folder ID({folder.folder_name}): {folder_id} is {total_size} bytes")
                return total_size
            except Exception as e:
                logger.error(f"Error in calculate_folder_size: {e}", exc_info=True)
                print("Something went wrong while calculating the folder size. Please check the log file for details.")
                raise
