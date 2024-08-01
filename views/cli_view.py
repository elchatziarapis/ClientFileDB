class CLIView:
    def display_basic_menu(self):
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

    def get_user_choice(self):
        return input("Enter your choice: ")