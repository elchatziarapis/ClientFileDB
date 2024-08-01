from logger import Logger
from services.file_service import FileService
from models.file import File

logger = Logger.get_logger()

class FileController:
    def __init__(self, file_service: FileService):
        """
        Initialize the FileController with a FileService.

        Args:
            file_service (FileService): An instance of FileService to manage file operations.
        """
        self.file_service = file_service

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
            Exception: If an error occurs during file creation.
        """
        try:
            logger.info(f"File Controller was called to create file: {name} (ID: {folder_id})")
            file = self.file_service.create_file(name, folder_id, file_content)
            return file
        except Exception as e:
            logger.error(f"Error creating file: {str(e)}", exc_info=True)
            print("Something went wrong while creating the file. Please check the log file for details.")
            raise

    def get_file_details(self, file_id: int) -> File:
        """
        Retrieve details of a file by its ID.

        Args:
            file_id (int): The ID of the file.

        Returns:
            File: The File object containing file details.

        Raises:
            Exception: If an error occurs during file retrieval.
        """
        try:
            file = self.file_service.get_file(file_id)
            logger.info(f"Retrieved file details: {file.file_name} (ID: {file.file_id})")
            return file
        except Exception as e:
            logger.error(f"Error retrieving file details: {str(e)}", exc_info=True)
            raise

    def delete_file(self, file_id: int) -> File:
        """
        Delete a file by its ID.

        Args:
            file_id (int): The ID of the file to be deleted.

        Raises:
            KeyError: If the file ID is invalid.
            Exception: If an error occurs during file deletion.
        """
        try:
            logger.info(f"File Controller was called to delete file ID: {file_id}")
            file = self.file_service.delete_file(file_id)
            return file
        except KeyError as e:
            logger.error(f"Invalid action selected: {str(e)}")
            print("Invalid action selected. Please check the log file for details.")
            raise
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}", exc_info=True)
            print("Something went wrong while deleting the file. Please check the log file for details.")
            raise

    def move_file(self, file_id: int, new_folder_id: int) -> File:
        """
        Move a file to a new folder.

        Args:
            file_id (int): The ID of the file to be moved.
            new_folder_id (int): The ID of the new folder.

        Returns:
            File: The moved File object.

        Raises:
            Exception: If an error occurs during file move.
        """
        try:
            file = self.file_service.move_file(file_id, new_folder_id)
            logger.info(f"Moved file ID: {file_id} to folder ID: {new_folder_id}")
            return file
        except Exception as e:
            logger.error(f"Error moving file: {str(e)}", exc_info=True)
            raise

    def download_file(self, file_id: int, local_path: str) -> str:
        """
        Download a file to a local path.

        Args:
            file_id (int): The ID of the file to be downloaded.
            local_path (str): The local path where the file will be saved.

        Returns:
            str: The local path where the file was saved.

        Raises:
            PermissionError: If there is a permission error during download.
            Exception: If an error occurs during file download.
        """
        try:
            logger.info(f"File Controller was called to download file ID: {file_id}")
            local_path = self.file_service.download_file(file_id, local_path)
            return local_path
        except PermissionError as e:
            logger.error(f"Permission error: {str(e)}", exc_info=True)
            print(f"Permission error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}", exc_info=True)
            print("Something went wrong while downloading the file. Please check the log file for details.")
            raise

    def create_file_from_local(self, local_file_path: str, folder_id: int) -> File:
        """
        Create a new file from a local file path in the specified folder.

        Args:
            local_file_path (str): The local path of the file to be uploaded.
            folder_id (int): The ID of the folder where the file will be created.

        Returns:
            File: The created File object.

        Raises:
            Exception: If an error occurs during file creation from the local path.
        """
        try:
            logger.info(f"File Controller was called to create file from local path: {local_file_path} (ID: {folder_id})")
            file = self.file_service.create_file_from_local(local_file_path, folder_id)
            return file
        except Exception as e:
            logger.error(f"Error creating file from local path: {str(e)}", exc_info=True)
            print("Something went wrong while creating the file from the local path. Please check the log file for details.")
            raise