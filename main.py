from injector import Injector
from controllers.file_controller import FileController
from controllers.folder_controller import FolderController
from views.cli_view import CLIView
from sqlalchemy.exc import IntegrityError, OperationalError, DataError
from utils.s3_utils import S3Utils
from logger import Logger
from app_dependcy_injector import AppInjector

logger = Logger.get_logger()

def main():
    """Main function to run the application."""
    injector = Injector([AppInjector])

    if not S3Utils.check_s3_connection():
        logger.error("S3 connection failed. Exiting application.")
        return

    file_controller = injector.get(FileController)
    folder_controller = injector.get(FolderController)
    view = CLIView()
    basic_actions = {
        '1': ('Create folder', folder_controller.create_folder, view.get_folder_details, view.display_create_folder),
        '2': ('Delete folder', folder_controller.delete_folder, view.get_folder_id, view.display_delete_folder),
        '3': ('Move folder', folder_controller.move_folder, view.get_move_details, view.display_move_folder),
        '4': ('List files and subfolders', folder_controller.list_files_and_subfolders, view.get_folder_id, view.display_list_files_and_subfolders),
        '5': ('Create file', file_controller.create_file, view.get_file_details, view.display_create_file),
        '6': ('Delete file', file_controller.delete_file, view.get_file_id, view.display_delete_file),
        '7': ('Move file', file_controller.move_file, view.get_move_details, view.display_move_file),
        '8': ('Get file details', file_controller.get_file_details, view.get_file_id, view.display_file_details),
        '9': ('Calculate folder size', folder_controller.calculate_folder_size, view.get_folder_id, lambda size: print(f"Total size of folder and its subfolders: {size} bytes"))
    }

    while True:
        try:
            view.display_basic_menu()
            basic_choice = view.get_user_choice()

            if basic_choice == '0':
                logger.info("Exiting application.")
                break

            basic_action = basic_actions.get(basic_choice)
            if basic_action:
                _, controller_method, input_method, display_method = basic_action
                inputs = input_method()
                result = controller_method(*inputs) if isinstance(inputs, tuple) else controller_method(inputs)
                display_method(result)
            else:
                view.display_invalid_choice()
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


if __name__ == "__main__":
    main()