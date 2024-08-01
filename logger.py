import logging

class Logger:
    """
    A simple logger class to configure and retrieve a logger instance.

    This logger ensures that only one handler is added to prevent duplicate log entries.
    It also removes all handlers associated with the root logger object to maintain clean logging.
    """
    @staticmethod
    def get_logger(log_file: str = "app.log") -> logging.Logger:
        """
        Configures and returns a logger instance.

        Parameters:
        log_file (str): The name of the log file. Default is "app.log".

        Returns:
        logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # Remove all handlers associated with the root logger object
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Check if the logger already has handlers to avoid adding multiple handlers
        if not logger.handlers:

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        return logger
