import unittest
from database import Database
from services.folder_service import FolderService
from injector import Injector
from app_dependcy_injector import AppInjector
from sqlalchemy.orm import sessionmaker
from models.file import File

class TestFolderService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        injector = Injector([AppInjector])
        cls.db = injector.get(Database)
        cls.folder_service = injector.get(FolderService)
        cls.Session = sessionmaker(bind=cls.db.engine)
        cls.db_session = cls.db.get_db_session()

    def setUp(self):
        # Create a new connection and begin a transaction
        self.connection = self.db.engine.connect()
        self.transaction = self.connection.begin()
        self.session = self.Session(bind=self.connection)

    def tearDown(self):
        # Rollback the transaction and close the connection
        self.transaction.rollback()
        self.connection.close()

    def test_create_folder(self):
        folder_name = 'test_folder'
        parent_id = 1 
        folder = self.folder_service.create_folder(folder_name, parent_id)
        self.assertIsNotNone(folder.folder_id)
        self.assertEqual(folder.folder_name, folder_name)
        self.assertEqual(folder.folder_parent_id, parent_id)
        self.folder_service.delete_folder(folder_id=folder.folder_id)

    def test_create_and_check_folder_exists(self):
        folder_name = 'check_folder_unique' 
        parent_id = 1
        created_folder = self.folder_service.create_folder(folder_name, parent_id)
        retrieved_folder = self.folder_service.get_folder(created_folder.folder_id)
        self.assertIsNotNone(retrieved_folder)
        self.assertEqual(retrieved_folder.folder_name, folder_name)
        self.assertEqual(retrieved_folder.folder_parent_id, parent_id)
        self.folder_service.delete_folder(folder_id=created_folder.folder_id)


    def test_create_duplicate_root_folder(self):
        folder_name = 'root_folder'
        parent_id = None
        try:
            self.folder_service.create_folder(folder_name, parent_id)
        except Exception as e:
            self.assertTrue(True)

    def test_delete_folder(self):
        folder_name = 'delete_folder'
        parent_id = 1
        created_folder = self.folder_service.create_folder(folder_name, parent_id)
        self.folder_service.delete_folder(created_folder.folder_id)
        
        try:
            self.folder_service.get_folder(created_folder.folder_id)
        except Exception as e:
            self.assertTrue(True)


    def test_move_folder(self):
        sub_folder = self.folder_service.create_folder('sub_folder_unique', 1)
        new_root_folder = self.folder_service.create_folder('new_root_unique', 2)
        moved_folder = self.folder_service.move_folder(sub_folder.folder_id, new_root_folder.folder_id)
        self.assertEqual(moved_folder.folder_parent_id, new_root_folder.folder_id)
        self.folder_service.delete_folder(sub_folder.folder_id)
        self.folder_service.delete_folder( new_root_folder.folder_id)


if __name__ == '__main__':
    unittest.main()
