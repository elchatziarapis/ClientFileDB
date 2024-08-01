import unittest
import os
import configparser
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from database import Database

class TestDatabase(unittest.TestCase):    
    @classmethod
    def setUpClass(cls):
        cls.config_path = 'config/config.ini'
        if not os.path.exists(cls.config_path):
            raise FileNotFoundError(f"Test configuration file '{cls.config_path}' does not exist.")
        cls.config = configparser.ConfigParser()
        cls.config.read(cls.config_path)
        cls.db = Database(config_path=cls.config_path)
    
    def test_database_url(self):
        dialect = self.config['database']['dialect']
        driver = self.config['database'].get('driver', '')
        host = self.config['database']['host']
        user = self.config['database']['user']
        password = self.config['database']['password']
        dbname = self.config['database']['dbname']
        driver_part = f"+{driver}" if driver else ""
        expected_url = f"{dialect}{driver_part}://{user}:{password}@{host}/{dbname}"
        self.assertEqual(self.db.DATABASE_URL, expected_url, "Database URL does not match the expected URL.")
    
    def test_engine_creation(self):
        self.assertIsNotNone(self.db.engine, "Engine should be created.")
        self.assertIsNotNone(self.db.SessionLocal, "SessionLocal should be created.")
    
    def test_database_accessibility(self):
        try:
            self.db._check_database_existence()
        except OperationalError:
            self.fail("Database is not accessible.")
    
    def test_init_db(self):
        try:
            self.db.init_db()
        except Exception as e:
            self.fail(f"init_db raised an exception: {e}")
    
    def test_get_db_session(self):
        session = self.db.get_db_session()
        self.assertIsNotNone(session, "Session should be created.")
        try:
            session.execute(text("SELECT 1"))
        except Exception as e:
            self.fail(f"Session execution raised an exception: {e}")
        finally:
            session.close()
    
    def test_close_db_session(self):
        session = self.db.get_db_session()
        try:
            self.db.close_db_session(session)
        except Exception as e:
            self.fail(f"close_db_session raised an exception: {e}")
    
    @classmethod
    def tearDownClass(cls):
        cls.db = None


if __name__ == '__main__':
    unittest.main()