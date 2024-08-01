from services.folder_service import FolderService
from models.folder import Folder
from typing import Dict
from logger import Logger

logger = Logger.get_logger()

class FolderController:
    """
    A controller class to handle folder-related operations.

    Attributes:
    folder_service (FolderService): An instance of the FolderService to perform business logic.
    """

    def __init__(self, folder_service: FolderService):
        """
        Initializes the FolderController with a FolderService instance.

        Parameters:
        folder_service (FolderService): The folder service instance to use for operations.
        """
        self.folder_service = folder_service

    def create_folder(self, name: str, parent_id: int) -> Folder:
        """
        Creates a new folder with the given name and parent ID.

        Parameters:
        name (str): The name of the new folder.
        parent_id (int): The ID of the parent folder.

        Returns:
        Folder: The created folder instance.

        Raises:
        Exception: If there is an error during folder creation.
        """
        try:
            folder = self.folder_service.create_folder(name, parent_id)
            logger.info(f"Folder Controller was called to create folder: {folder.folder_name} (ID: {folder.folder_id})")
            return folder
        except Exception as e:
            logger.error(f"Error creating folder: {str(e)}", exc_info=True)
            raise

    def get_folder_details(self, folder_id: int) -> Folder:
        """
        Retrieves the details of a folder by its ID.

        Parameters:
        folder_id (int): The ID of the folder.

        Returns:
        Folder: The folder instance with the specified ID.

        Raises:
        Exception: If there is an error retrieving the folder details.
        """
        try:
            folder = self.folder_service.get_folder(folder_id)
            logger.info(f"Folder Controller was called to get details for folder ID: {folder_id}")
            return folder
        except Exception as e:
            logger.error(f"Error retrieving folder details: {str(e)}", exc_info=True)
            raise

    def delete_folder(self, folder_id: int):
        """
        Deletes a folder by its ID.

        Parameters:
        folder_id (int): The ID of the folder to delete.

        Raises:
        Exception: If there is an error during folder deletion.
        """
        try:
            folder_data = self.folder_service.delete_folder(folder_id)
            logger.info(f"Folder Controller was called to delete folder ID: {folder_id}")
            return folder_data
        except Exception as e:
            logger.error(f"Error deleting folder: {str(e)}", exc_info=True)
            raise

    def move_folder(self, folder_id: int, new_parent_id: int) -> Folder:
        """
        Moves a folder to a new parent folder.

        Parameters:
        folder_id (int): The ID of the folder to move.
        new_parent_id (int): The ID of the new parent folder.

        Returns:
        Folder: The moved folder instance.

        Raises:
        Exception: If there is an error during the folder move.
        """
        try:
            folder = self.folder_service.move_folder(folder_id, new_parent_id)
            logger.info(f"Folder Controller was called to move folder ID: {folder_id} to parent ID: {new_parent_id}")
            return folder
        except Exception as e:
            logger.error(f"Error moving folder: {str(e)}", exc_info=True)
            raise

    def list_files_and_subfolders(self, folder_id: int) -> Dict:
        """
        Lists all files and subfolders within a folder.

        Parameters:
        folder_id (int): The ID of the folder to list contents for.

        Returns:
        List[Union[File, Folder]]: A list of files and subfolders within the specified folder.

        Raises:
        Exception: If there is an error listing the files and subfolders.
        """
        try:
            contents = self.folder_service.list_files_and_subfolders(folder_id)
            logger.info(f"Folder Controller was called to list files and subfolders for folder ID: {folder_id}")
            return contents
        except Exception as e:
            logger.error(f"Error listing files and subfolders: {str(e)}", exc_info=True)
            raise