from sqlalchemy import (
    Column, 
    Integer,
    String, 
    ForeignKey, 
    Index,
    UniqueConstraint, 
    CheckConstraint
)

from sqlalchemy.orm import (
    relationship, 
    backref, 
    declarative_base
)

Base = declarative_base()

class Folder(Base):
    """
    A SQLAlchemy ORM class representing the 'folders' table in the database.

    Attributes:
    folder_id (int): Primary key of the folder.
    folder_name (str): Name of the folder, cannot be null.
    folder_parent_id (int): ID of the parent folder, can be null if it's a root folder.
    children (relationship): Relationship to child folders.
    files (relationship): Relationship to files within the folder.
    """

    __tablename__ = 'folders'

    folder_id = Column(Integer, primary_key=True)
    folder_name = Column(String(255), nullable=False)
    folder_parent_id = Column(Integer, ForeignKey('folders.folder_id', ondelete='CASCADE'), nullable=True)

    children = relationship(
        "Folder",
        backref=backref('parent', remote_side=[folder_id]),
        cascade='all, delete-orphan',
        single_parent=True,
        lazy='joined'  # Ensure joined loading strategy
    )
    files = relationship("File", backref='folder', cascade='all, delete-orphan')

    __table_args__ = (
        UniqueConstraint('folder_parent_id', 'folder_name', name='unique_folder_name_per_parent'),
        CheckConstraint('folder_id <> folder_parent_id', name='no_self_reference'),
        Index('idx_folder_parent_id', 'folder_parent_id')
    )

    def __repr__(self):
        return f"<Folder(folder_id={self.folder_id}, folder_name={self.folder_name}, folder_parent_id={self.folder_parent_id})>"
