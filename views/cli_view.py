from typing import List, Dict, Tuple

class CLIView:
    """
    A class to handle the command-line interface for folder and file operations.
    """

    def display_basic_menu(self):
        """
        Display the basic menu for folder and file operations.
        """
        print("\n--- Basic Folder and File Operations ---")
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
        name = input("Enter folder name: ")
        parent_id = int(input("Enter parent folder ID (0 for root): "))
        return (name, parent_id)
    
    def display_create_folder(self, folder):
        """
        Display the details of the created folder.

        Args:
            folder (Folder): The created folder object.
        """
        print(f"Folder created: {folder.folder_name} (ID: {folder.folder_id})")

    def display_folder_details(self, folder):
        """
        Display the details of a folder.

        Args:
            folder (Folder): The folder object.
        """
        print(f"Folder details - ID: {folder.folder_id}, Name: {folder.folder_name}, Parent ID: {folder.folder_parent_id}")

    def display_delete_folder(self, deleted_items: List[Dict]):
        """
        Display the details of all deleted folders and files.

        Args:
            deleted_items (List[Dict]): A list of dictionaries representing the deleted folders and files.
        """
        for item in deleted_items:
            if item['type'] == 'folder':
                print(f"Deleted folder ID: {item['id']}, Name: {item['name']}")
            elif item['type'] == 'file':
                print(f"Deleted file ID: {item['id']}, Name: {item['name']}, S3 Key: {item['s3_key']}")

    def display_move_folder(self, folder):
        """
        Display the details of the moved folder.

        Args:
            folder (Folder): The moved folder object.
        """
        print(f"Moved folder ID: {folder.folder_id}, Name: {folder.folder_name} to parent ID: {folder.folder_parent_id}")

    def display_create_file(self, file):
        """
        Display the details of the created file.

        Args:
            file (File): The created file object.
        """
        print(f"File created: {file.file_name} (ID: {file.file_id})")

    def get_folder_id(self) -> int:
        """
        Get the folder ID from the user.

        Returns:
            int: The folder ID.
        """
        folder_id = int(input("Enter folder ID: "))
        return folder_id
    
    def get_move_details(self) -> Tuple[int, int]:
        """
        Get the details for moving a folder from the user.

        Returns:
            Tuple[int, int]: A tuple containing the folder ID and the new parent folder ID.
        """
        folder_id = int(input("Enter folder ID: "))
        new_parent_id = int(input("Enter new parent folder ID: "))
        return (folder_id, new_parent_id)

    def display_list_files_and_subfolders(self, contents: Dict, level: int = 0):
        """
        Display the list of files and subfolders within a folder recursively.

        Args:
            contents (Dict): A dictionary containing files and subfolders.
            level (int): The current level of indentation for nested subfolders. Default is 0.
        """
        indent = "    " * level

        print(f"{indent}--- Files ---")
        for file in contents['Files']:
            print(f"{indent}ID: {file['File ID']}, Name: {file['File Name']}, Size: {file['File Size']} bytes")
        
        print(f"{indent}--- Subfolders ---")
        for subfolder in contents['Subfolders']:
            print(f"{indent}ID: {subfolder['Folder ID']}, Name: {subfolder['Folder Name']}")
            self.display_list_files_and_subfolders(subfolder, level + 1)
