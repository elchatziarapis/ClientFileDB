from views.cli_view import CLIView
from logger import Logger

logger = Logger.get_logger()

def main():

    view = CLIView()

    basic_actions = {
        '1': ('Create folder',),
        '2': ('Delete folder',),
        '3': ('Move folder',),
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
                display_method = basic_action
            else:
                view.display_invalid_choice()
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()