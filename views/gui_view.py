import tkinter as tk
from tkinter import simpledialog, scrolledtext, filedialog
from typing import List, Dict, Tuple
from controllers.file_controller import FileController
from controllers.folder_controller import FolderController
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from logger import Logger

logger = Logger.get_logger()

class CustomInputDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, prompt=None):
        self.prompt = prompt
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text=self.prompt).pack(padx=5, pady=5)
        self.input_var = tk.StringVar()
        self.entry = tk.Entry(master, textvariable=self.input_var)
        self.entry.pack(padx=5, pady=5)
        self.entry.focus_set()
        return self.entry

    def apply(self):
        self.result = self.input_var.get()

class CustomIntInputDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, prompt=None):
        self.prompt = prompt
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text=self.prompt).pack(padx=5, pady=5)
        self.input_var = tk.IntVar()
        self.entry = tk.Entry(master, textvariable=self.input_var)
        self.entry.pack(padx=5, pady=5)
        self.entry.focus_set()
        return self.entry

    def apply(self):
        self.result = self.input_var.get()

class CustomChoiceDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, prompt=None, choices=None):
        self.prompt = prompt
        self.choices = choices or []
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text=self.prompt).pack(padx=5, pady=5)
        self.choice_var = tk.StringVar(value=self.choices[0])
        for choice in self.choices:
            tk.Radiobutton(master, text=choice, variable=self.choice_var, value=choice).pack(anchor=tk.W)
        return master

    def apply(self):
        self.result = self.choice_var.get()

class GUIView:
    def __init__(self, root, file_controller: FileController, folder_controller: FolderController):
        self.root = root
        self.file_controller = file_controller
        self.folder_controller = folder_controller
        self.separator_length = 70 
        
        self.basic_actions = {
            'Create Folder': (self.folder_controller.create_folder, self.get_folder_details, self.display_create_folder),
            'Delete Folder': (self.folder_controller.delete_folder, self.get_folder_id, self.display_delete_folder),
            'Move Folder': (self.folder_controller.move_folder, self.get_move_details, self.display_move_folder),
            'List Files and Subfolders': (self.folder_controller.list_files_and_subfolders, self.get_folder_id, self.display_list_files_and_subfolders),
            'Create File': (self.file_controller.create_file, self.get_file_details, self.display_create_file),
            'Delete File': (self.file_controller.delete_file, self.get_file_id, self.display_delete_file),
            'Move File': (self.file_controller.move_file, self.get_file_move_details, self.display_move_file),
            'Get File Details': (self.file_controller.get_file_details, self.get_file_id, self.display_file_details),
            'Calculate Folder Size': (self.folder_controller.calculate_folder_size, self.get_folder_id, self.display_folder_size)
        }
        
        self.create_widgets()

    def create_widgets(self):
        self.root.title("Basic Folder and File Operations")
        self.root.geometry("1200x800")
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.menu_frame = tk.Frame(self.main_frame)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        self.action_buttons = []
        for action in self.basic_actions.keys():
            btn = tk.Button(self.menu_frame, text=action, width=30, command=lambda a=action: self.execute_action(a))
            btn.pack(pady=5)
            self.action_buttons.append(btn)

        self.exit_button = tk.Button(self.menu_frame, text="Exit", width=30, command=self.root.quit)
        self.exit_button.pack(pady=5)
        
        self.result_frame = tk.Frame(self.main_frame)
        self.result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.result_label = tk.Label(self.result_frame, text="Results")
        self.result_label.pack(anchor=tk.N)

        self.result_box = scrolledtext.ScrolledText(self.result_frame, wrap=tk.WORD, width=80, height=40)
        self.result_box.pack(fill=tk.BOTH, expand=True)

    def execute_action(self, action):
        try:
            controller_method, input_method, display_method = self.basic_actions[action]
            inputs = input_method()
            result = controller_method(*inputs) if isinstance(inputs, tuple) else controller_method(inputs)
            display_method(result)
        except IntegrityError as e:
            logger.error(f"Database integrity error: {str(e)}")
            self.result_box.insert(tk.END, f"Error: Database integrity error: {str(e)}\n")
        except OperationalError as e:
            logger.error(f"Operational error: {str(e)}")
            self.result_box.insert(tk.END, f"Error: Operational error: {str(e)}\n")
        except DataError as e:
            logger.error(f"Data error: {str(e)}")
            self.result_box.insert(tk.END, f"Error: Data error: {str(e)}\n")
        except KeyError as e:
            logger.error(f"Invalid action selected: {str(e)}")
            self.result_box.insert(tk.END, f"Error: Invalid action selected: {str(e)}\n")
        except ValueError as e:
            logger.error(f"Value error: {str(e)}")
            self.result_box.insert(tk.END, f"Error: Value error: {str(e)}\n")
        except TypeError as e:
            logger.error(f"Type error: {str(e)}")
            self.result_box.insert(tk.END, f"Error: Type error: {str(e)}\n")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            self.result_box.insert(tk.END, f"Error: An unexpected error occurred: {str(e)}\n")

    def get_folder_details(self) -> Tuple[str, int]:
        name = CustomInputDialog(self.root, title="Create New Folder", prompt="Enter folder name:").result
        parent_id = CustomIntInputDialog(self.root, title="Create New Folder", prompt="Enter parent folder ID (0 for root):").result
        return (name, parent_id)

    def get_folder_id(self) -> int:
        folder_id = CustomIntInputDialog(self.root, title="Enter Folder ID", prompt="Enter folder ID:").result
        return folder_id

    def get_file_move_details(self) -> Tuple[int, int]:
        file_id = CustomIntInputDialog(self.root, title="Move File", prompt="Enter file ID:").result
        new_parent_id = CustomIntInputDialog(self.root, title="Move File", prompt="Enter new folder ID:").result
        return (file_id, new_parent_id)

    def get_move_details(self) -> Tuple[int, int]:
        folder_id = CustomIntInputDialog(self.root, title="Move Folder", prompt="Enter folder ID:").result
        new_parent_id = CustomIntInputDialog(self.root, title="Move Folder", prompt="Enter new parent folder ID:").result
        return (folder_id, new_parent_id)

    def get_file_id(self) -> int:
        file_id = CustomIntInputDialog(self.root, title="Enter File ID", prompt="Enter file ID:").result
        return file_id

    def get_file_details(self) -> Tuple[str, int, bytes]:
        folder_id = CustomIntInputDialog(self.root, title="Create New File", prompt="Enter folder ID:").result
        
        choice = CustomChoiceDialog(
            self.root, 
            title="Create New File", 
            prompt="Would you like to input text or upload a file?", 
            choices=["Input Text", "Upload File"]
        ).result
        
        if choice == "Input Text":
            file_content = CustomInputDialog(self.root, title="Input File Content", prompt="Enter file content:").result.encode('utf-8')
            name = CustomInputDialog(self.root, title="Create New File", prompt="Enter file name:").result
        elif choice == "Upload File":
            file_path = filedialog.askopenfilename(title="Select a file to upload")
            with open(file_path, 'rb') as file:
                file_content = file.read()
            default_name = file_path.split('/')[-1]
            name_choice = CustomChoiceDialog(
                self.root,
                title="File Name",
                prompt=f"Use the default name '{default_name}' or provide a new name?",
                choices=["Use Default Name", "Provide New Name"]
            ).result
            
            if name_choice == "Use Default Name":
                name = default_name
            else:
                name = CustomInputDialog(self.root, title="Rename File", prompt="Enter new file name:").result
        
        return (name, folder_id, file_content)

    def display_create_folder(self, folder):
        self.result_box.insert(tk.END, f"{'Folder Created':<20} | {'Name':<20}: {folder.folder_name}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'ID':<20}: {folder.folder_id}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'Parent ID':<20}: {folder.folder_parent_id}\n")
        self.result_box.insert(tk.END, f"{'-' * 50}\n\n")

    def display_folder_details(self, folder):
        self.result_box.insert(tk.END, f"{'Folder Details':<20} | {'ID':<20}: {folder.folder_id}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'Name':<20}: {folder.folder_name}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'Parent ID':<20}: {folder.folder_parent_id}\n")
        self.result_box.insert(tk.END, f"{'-' * 50}\n\n")

    def display_delete_folder(self, deleted_items: List[Dict]):
        self.result_box.insert(tk.END, f"{'Deleted Items':<20}\n")
        for item in deleted_items:
            if item['type'] == 'folder':
                self.result_box.insert(tk.END, f"{'Folder':<20} | {'ID':<20}: {item['id']}\n")
                self.result_box.insert(tk.END, f"{'':<20} | {'Name':<20}: {item['name']}\n")
            elif item['type'] == 'file':
                self.result_box.insert(tk.END, f"{'File':<20} | {'ID':<20}: {item['id']}\n")
                self.result_box.insert(tk.END, f"{'':<20} | {'Name':<20}: {item['name']}\n")
                self.result_box.insert(tk.END, f"{'':<20} | {'S3 Key':<20}: {item['s3_key']}\n")
            self.result_box.insert(tk.END, f"{'-' * 50}\n")
        self.result_box.insert(tk.END, f"\n")

    def display_move_folder(self, folder):
        self.result_box.insert(tk.END, f"{'Moved Folder':<20} | {'Name':<20}: {folder.folder_name}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'ID':<20}: {folder.folder_id}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'New Parent ID':<20}: {folder.folder_parent_id}\n")
        self.result_box.insert(tk.END, f"{'-' * 50}\n\n")

    def display_create_file(self, file):
        self.result_box.insert(tk.END, f"{'File Created':<20} | {'Name':<20}: {file.file_name}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'ID':<20}: {file.file_id}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'Folder ID':<20}: {file.folder_id}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'Size':<20}: {file.file_size} bytes\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'Created Date':<20}: {file.file_created_date}\n")
        self.result_box.insert(tk.END, f"{'-' * 50}\n\n")

    def display_delete_file(self, file):
        self.result_box.insert(tk.END, f"{'Deleted File':<20} | {'Name':<20}: {file.file_name}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'ID':<20}: {file.file_id}\n")
        self.result_box.insert(tk.END, f"{'-' * 50}\n\n")

    def display_move_file(self, file):
        self.result_box.insert(tk.END, f"{'Moved File':<20} | {'Name':<20}: {file.file_name}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'ID':<20}: {file.file_id}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'New Folder ID':<20}: {file.folder_id}\n")
        self.result_box.insert(tk.END, f"{'-' * 50}\n\n")

    def display_file_details(self, file):
        self.result_box.insert(tk.END, f"{'File Details':<20} | {'ID':<20}: {file.file_id}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'Name':<20}: {file.file_name}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'Size':<20}: {file.file_size} bytes\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'Created Date':<20}: {file.file_created_date}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'S3 Key':<20}: {file.file_s3_key}\n")
        self.result_box.insert(tk.END, f"{'':<20} | {'Folder ID':<20}: {file.folder_id}\n")
        self.result_box.insert(tk.END, f"{'-' * 50}\n\n")

    def display_folder_size(self, size: int):
        self.result_box.insert(tk.END, f"Total size of folder and its subfolders: {size} bytes\n\n")

    def display_list_files_and_subfolders(self, contents: Dict, level: int = 0):
        details = self.format_list_files_and_subfolders(contents, level)
        self.result_box.insert(tk.END, f"Files and Subfolders:\n{details}\n\n")

    def format_list_files_and_subfolders(self, contents: Dict, level: int = 0) -> str:
        indent = "    " * level
        result = []

        result.append(f"{indent}--- Subfolders ---")
        for subfolder in contents['Subfolders']:
            result.append(f"{indent}ID: {subfolder['Folder ID']:<10} | Name: {subfolder['Folder Name']}")
            result.append(self.format_list_files_and_subfolders(subfolder, level + 1))

        result.append(f"{indent}--- Files ---")
        for file in contents['Files']:
            result.append(f"{indent}ID: {file['File ID']:<10} | Name: {file['File Name']:<30} | Size: {file['File Size']} bytes")

        return "\n".join(result)
