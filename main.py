from views.cli_view import CLIView
from controllers.folder_controller import FolderController
from logger import Logger
from injector import Injector
from app_dependcy_injector import AppInjector
from models.file import File

logger = Logger.get_logger()

def main():
    injector = Injector([AppInjector])
    folder_controller = injector.get(FolderController)
    view = CLIView()

    basic_actions = {
        '1': ('Create folder', folder_controller.create_folder, view.get_folder_details, view.display_create_folder),
        '2': ('Delete folder', folder_controller.delete_folder, view.get_folder_id, view.display_delete_folder),
        '3': ('Move folder', folder_controller.move_folder, view.get_move_details, view.display_move_folder),
        '4': ('List files and subfolders',),
        '5': ('Create file',),
        '6': ('Delete file',),
        '7': ('Move file',),
        '8': ('Get file details',),
        '9': ('Calculate folder size(recursive)',)
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
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()