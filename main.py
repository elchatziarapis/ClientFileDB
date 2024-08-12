import argparse
import tkinter as tk
from injector import Injector
from controllers.file_controller import FileController
from controllers.folder_controller import FolderController
from utils.s3_utils import S3Utils
from logger import Logger
from app_dependcy_injector import AppInjector
from views.cli_view import CLIView
from views.gui_view import GUIView

logger = Logger.get_logger()

def main():
    """Main function to run the application."""
    parser = argparse.ArgumentParser(description="Choose between CLI and GUI")
    parser.add_argument('--mode', choices=['cli', 'gui'], required=True, help="Choose the interface mode: cli or gui")
    args = parser.parse_args()

    injector = Injector([AppInjector])

    if not S3Utils.check_s3_connection():
        logger.error("S3 connection failed. Exiting application.")
        return

    file_controller = injector.get(FileController)
    folder_controller = injector.get(FolderController)

    if args.mode == 'cli':
        view = CLIView(file_controller, folder_controller)
        view.run()
    elif args.mode == 'gui':
        root = tk.Tk()
        app = GUIView(root, file_controller, folder_controller)
        root.mainloop()

if __name__ == "__main__":
    main()
