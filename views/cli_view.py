from typing import List, Dict, Tuple
from controllers.file_controller import FileController
from controllers.folder_controller import FolderController
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from logger import Logger

logger = Logger.get_logger()

class CLIView:
    """
    A class to handle the command-line interface for folder and file operations.

    Attributes:
        file_controller (FileController): The controller to manage file operations.
        folder_controller (FolderController): The controller to manage folder operations.
        separator_length (int): The length of the separators used in the display.
        basic_actions (dict): A dictionary mapping user choices to corresponding actions.
    """

    def __init__(self, file_controller: FileController, folder_controller: FolderController):
        """
        Initialize the CLIView with the given controllers.

        Args:
            file_controller (FileController): The controller to manage file operations.
            folder_controller (FolderController): The controller to manage folder operations.
        """
        self.separator_length = 70
        self.file_controller = file_controller
        self.folder_controller = folder_controller
        self.basic_actions = {
            '1': ('Create folder', self.folder_controller.create_folder, self.get_folder_details, self.display_create_folder),
            '2': ('Delete folder', self.folder_controller.delete_folder, self.get_folder_id, self.display_delete_folder),
            '3': ('Move folder', self.folder_controller.move_folder, self.get_move_details, self.display_move_folder),
            '4': ('List files and subfolders', self.folder_controller.list_files_and_subfolders, self.get_folder_id, self.display_list_files_and_subfolders),
            '5': ('Create file', self.file_controller.create_file, self.get_file_details, self.display_create_file),
            '6': ('Delete file', self.file_controller.delete_file, self.get_file_id, self.display_delete_file),
            '7': ('Move file', self.file_controller.move_file, self.get_file_move_details, self.display_move_file),
            '8': ('Get file details', self.file_controller.get_file_details, self.get_file_id, self.display_file_details),
            '9': ('Calculate folder size', self.folder_controller.calculate_folder_size, self.get_folder_id, lambda size: print(f"Total size of folder and its subfolders: {size} bytes"))
        }

    def display_basic_menu(self):
        """
        Display the basic menu for folder and file operations.
        """
        print("\n" + "=" * self.separator_length)
        print(" Basic Folder and File Operations ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        print("1. Create a new folder")
        print("2. Delete an existing folder")
        print("3. Move a folder to a different location")
        print("4. List all files and subfolders within a folder")
        print("5. Create a new file within a specified folder")
        print("6. Delete an existing file")
        print("7. Move a file to a different folder")
        print("8. Retrieve file details (name, size, creation date)")
        print("9. Retrieve the total size of all files within a folder and its subfolders")
        print("0. Exit")
        print("=" * self.separator_length)

    def get_user_choice(self) -> str:
        """
        Get the user's menu choice.

        Returns:
            str: The user's choice.
        """
        return input("Enter your choice: ")

    def get_folder_details(self) -> Tuple[str, int]:
        """
        Get the details for creating a new folder from the user.

        Returns:
            Tuple[str, int]: A tuple containing the folder name and parent folder ID.
        """
        print("\n" + "=" * self.separator_length)
        print(" Create New Folder ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        name = input("Enter folder name: ")
        parent_id = int(input("Enter parent folder ID (0 for root): "))
        print("=" * self.separator_length)
        return (name, parent_id)

    def display_create_folder(self, folder):
        """
        Display the details of the created folder.

        Args:
            folder (Folder): The created folder object.
        """
        print("\n" + "=" * self.separator_length)
        print(" Folder Created! ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        print(f"Name: {folder.folder_name}")
        print(f"ID: {folder.folder_id}")
        print(f"Parent ID: {folder.folder_parent_id}")
        print(f"Created Date: {folder.folder_created_date}")
        print("=" * self.separator_length)

    def display_folder_details(self, folder):
        """
        Display the details of a folder.

        Args:
            folder (Folder): The folder object.
        """
        print("\n" + "=" * self.separator_length)
        print(" Folder Details ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        print(f"ID: {folder.folder_id}")
        print(f"Name: {folder.folder_name}")
        print(f"Parent ID: {folder.folder_parent_id}")
        print(f"Created Date: {folder.folder_created_date}")
        print("=" * self.separator_length)

    def display_delete_folder(self, deleted_items: List[Dict]):
        """
        Display the details of all deleted folders and files.

        Args:
            deleted_items (List[Dict]): A list of dictionaries representing the deleted folders and files.
        """
        print("\n" + "=" * self.separator_length)
        print(" Deleted Items ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        for item in deleted_items:
            if item['type'] == 'folder':
                print(f"Deleted Folder: ID: {item['id']}, Name: {item['name']}")
            elif item['type'] == 'file':
                print(f"Deleted File: ID: {item['id']}, Name: {item['name']}, S3 Key: {item['s3_key']}")
        print("=" * self.separator_length)

    def display_move_folder(self, folder):
        """
        Display the details of the moved folder.

        Args:
            folder (Folder): The moved folder object.
        """
        print("\n" + "=" * self.separator_length)
        print(" Moved Folder ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        print(f"Name: {folder.folder_name}")
        print(f"ID: {folder.folder_id}")
        print(f"New Parent ID: {folder.folder_parent_id}")
        print("=" * self.separator_length)

    def display_create_file(self, file):
        """
        Display the details of the created file.

        Args:
            file (File): The created file object.
        """
        print("\n" + "=" * self.separator_length)
        print(" File Created! ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        print(f"Name: {file.file_name}")
        print(f"ID: {file.file_id}")
        print(f"Folder ID: {file.folder_id}")
        print(f"Size: {file.file_size} bytes")
        print(f"Created Date: {file.file_created_date}")
        print("=" * self.separator_length)

    def get_folder_id(self) -> int:
        """
        Get the folder ID from the user.

        Returns:
            int: The folder ID.
        """
        print("\n" + "=" * self.separator_length)
        print(" Enter Folder ID ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        folder_id = int(input("Enter folder ID: "))
        print("=" * self.separator_length)
        return folder_id

    def get_file_move_details(self) -> Tuple[int, int]:
        """
        Get the details for moving a file from the user.

        Returns:
            Tuple[int, int]: A tuple containing the file ID and the new folder ID.
        """
        print("\n" + "=" * self.separator_length)
        print(" Move File ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        file_id = int(input("Enter file ID: "))
        new_folder_id = int(input("Enter new folder ID: "))
        print("=" * self.separator_length)
        return (file_id, new_folder_id)

    def get_move_details(self) -> Tuple[int, int]:
        """
        Get the details for moving a folder from the user.

        Returns:
            Tuple[int, int]: A tuple containing the folder ID and the new parent folder ID.
        """
        print("\n" + "=" * self.separator_length)
        print(" Move Folder ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        folder_id = int(input("Enter folder ID: "))
        new_parent_id = int(input("Enter new parent folder ID: "))
        print("=" * self.separator_length)
        return (folder_id, new_parent_id)

    def get_file_id(self) -> int:
        """
        Get the file ID from the user.

        Returns:
            int: The file ID.
        """
        print("\n" + "=" * self.separator_length)
        print(" Enter File ID ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        file_id = int(input("Enter file ID: "))
        print("=" * self.separator_length)
        return file_id

    def get_file_details(self) -> Tuple[str, int, bytes]:
        """
        Get the details for creating a new file from the user.

        Returns:
            Tuple[str, int, bytes]: A tuple containing the file name, folder ID, and file content.
        """
        print("\n" + "=" * self.separator_length)
        print(" Create New File ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        folder_id = int(input("Enter folder ID: "))
        
        choice = input("Would you like to input text or upload a file? (Enter '1' for text, '2' for upload): ")
        
        if choice == '1':
            file_content = input("Enter file content: ").encode('utf-8')
            name = input("Enter file name: ")
        elif choice == '2':
            file_path = input("Enter the path to the file you want to upload: ")
            with open(file_path, 'rb') as file:
                file_content = file.read()
            default_name = file_path.split('/')[-1]
            name_choice = input(f"Use the default name '{default_name}' or provide a new name? (Enter '1' for default, '2' for new name): ")
            if name_choice == '1':
                name = default_name
            else:
                name = input("Enter new file name: ")

        print("=" * self.separator_length)
        return (name, folder_id, file_content)

    def display_delete_file(self, file):
        """
        Display the details of the deleted file.

        Args:
            file (File): The deleted file object.
        """
        print("\n" + "=" * self.separator_length)
        print(" Deleted File ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        print(f"Name: {file.file_name}")
        print(f"ID: {file.file_id}")
        print("=" * self.separator_length)

    def display_move_file(self, file):
        """
        Display the details of the moved file.

        Args:
            file (File): The moved file object.
        """
        print("\n" + "=" * self.separator_length)
        print(" Moved File ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        print(f"Name: {file.file_name}")
        print(f"ID: {file.file_id}")
        print(f"New Folder ID: {file.folder_id}")
        print("=" * self.separator_length)

    def display_list_files_and_subfolders(self, contents: Dict, level: int = 0):
        """
        Display the list of files and subfolders within a folder recursively.

        Args:
            contents (Dict): A dictionary containing files and subfolders.
            level (int): The current level of indentation for nested subfolders. Default is 0.
        """
        indent = "    " * level

        print(f"{indent}" + "-" * self.separator_length)
        print(f"{indent}--- Subfolders ---")
        for subfolder in contents['Subfolders']:
            print(f"{indent}ID: {subfolder['Folder ID']}, Name: {subfolder['Folder Name']}")
            self.display_list_files_and_subfolders(subfolder, level + 1)

        print(f"{indent}--- Files ---")
        for file in contents['Files']:
            print(f"{indent}ID: {file['File ID']}, Name: {file['File Name']}, Size: {file['File Size']} bytes")
        print(f"{indent}" + "-" * self.separator_length)

    def display_file_details(self, file):
        """
        Display the details of a file.

        Args:
            file (File): The file object.
        """
        print("\n" + "=" * self.separator_length)
        print(" File Details ".center(self.separator_length, "="))
        print("=" * self.separator_length)
        print(f"ID: {file.file_id}")
        print(f"Name: {file.file_name}")
        print(f"Size: {file.file_size} bytes")
        print(f"Created Date: {file.file_created_date}")
        print(f"S3 Key: {file.file_s3_key}")
        print(f"Folder ID: {file.folder_id}")
        print("=" * self.separator_length)

    def run(self):
        """
        Run the command-line interface.
        """
        while True:
            try:
                self.display_basic_menu()
                basic_choice = self.get_user_choice()

                if basic_choice == '0':
                    logger.info("Exiting application.")
                    break

                basic_action = self.basic_actions.get(basic_choice)
                if basic_action:
                    _, controller_method, input_method, display_method = basic_action
                    inputs = input_method()
                    result = controller_method(*inputs) if isinstance(inputs, tuple) else controller_method(inputs)
                    display_method(result)
                else:
                    print("Invalid choice. Please select a valid option.")
            except IntegrityError as e:
                logger.error(f"Database integrity error: {str(e)}")
            except OperationalError as e:
                logger.error(f"Operational error: {str(e)}")
            except DataError as e:
                logger.error(f"Data error: {str(e)}")
            except KeyError as e:
                logger.error(f"Invalid action selected: {str(e)}")
            except ValueError as e:
                logger.error(f"Value error: {str(e)}")
            except TypeError as e:
                logger.error(f"Type error: {str(e)}")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {str(e)}")
