from logger import Logger
from services.file_service import FileService
from models.file import File

logger = Logger.get_logger()

class FileController:
    def __init__(self, file_service: FileService):
        self.file_service = file_service