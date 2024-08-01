from sqlalchemy import (Column, 
                        Integer, 
                        String, 
                        ForeignKey, 
                        Index, 
                        UniqueConstraint,
                        TIMESTAMP, 
                        func)
from database import Base

class File(Base):
    """
    A SQLAlchemy ORM class representing the 'files' table in the database.

    Attributes:
    file_id (int): Primary key of the file.
    file_name (str): Name of the file, cannot be null.
    file_size (int): Size of the file in bytes, cannot be null.
    file_created_date (timestamp): Timestamp when the file was created, defaults to the current time.
    folder_id (int): ID of the folder containing this file, cannot be null.
    file_s3_key (str): Unique S3 key for the file, cannot be null and must be unique.
    """

    __tablename__ = 'files'

    file_id = Column(Integer, primary_key=True)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_created_date = Column(TIMESTAMP, server_default=func.current_timestamp())
    folder_id = Column(Integer, ForeignKey('folders.folder_id'), nullable=False)
    file_s3_key = Column(String(255), nullable=False, unique=True)

    __table_args__ = (
        UniqueConstraint('folder_id', 'file_name', name='unique_file_name_per_folder'),
        Index('idx_file_folder_id', 'folder_id'),
        Index('idx_file_s3_key', 'file_s3_key')
    )

    def __repr__(self):
        return (f"<File(file_id={self.file_id}, file_name={self.file_name}, file_size={self.file_size}, "
                f"file_created_date={self.file_created_date}, folder_id={self.folder_id}, "
                f"file_s3_key={self.file_s3_key})>")
