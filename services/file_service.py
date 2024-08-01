from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.file import File
from database import Database
from logger import Logger

logger = Logger.get_logger()


class FileService:
    def __init__(self, db: Database):
        self.db = db
