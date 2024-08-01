import os
import configparser
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from logger import Logger

# Configure logging
logger = Logger.get_logger()

# Define the Base class for model definitions
Base = declarative_base()

class Database:
    """
    A class to handle database connections and operations using SQLAlchemy.

    Attributes:
    config_path (str): Path to the configuration file.
    config (ConfigParser): ConfigParser object to read the configuration file.
    DATABASE_URL (str): Database connection URL.
    engine (Engine): SQLAlchemy Engine object.
    SessionLocal (scoped_session): SQLAlchemy scoped session factory.
    Base (declarative_base): SQLAlchemy base class for models.
    _active_session (Session): Tracker for the active session.
    """

    def __init__(self, config_path='config/config.ini'):
        """
        Initializes the Database object and sets up the database connection.

        Parameters:
        config_path (str): Path to the configuration file. Default is 'config/config.ini'.

        Raises:
        FileNotFoundError: If the configuration file does not exist.
        KeyError: If required configuration options are missing.
        """
        if not os.path.exists(config_path):
            logger.error(f"Configuration file '{config_path}' does not exist.")
            raise FileNotFoundError(f"Configuration file '{config_path}' does not exist.")
        
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        logger.info("Configuration file read successfully.")
        
        self._setup_database_url()
        self._setup_engine_and_session()
        
        self._active_session = None

        self._check_database_existence()

    def _setup_database_url(self):
        """
        Sets up the database connection URL from the configuration file.

        Raises:
        KeyError: If required configuration options are missing.
        """
        try:
            dialect = self.config['database']['dialect']
            driver = self.config['database'].get('driver', '')
            host = self.config['database']['host']
            user = self.config['database']['user']
            password = self.config['database']['password']
            dbname = self.config['database']['dbname']
            driver_part = f"+{driver}" if driver else ""
            self.DATABASE_URL = f"{dialect}{driver_part}://{user}:{password}@{host}/{dbname}"
            logger.info(f"Database URL: {dialect}{driver_part}://{user}:********@{host}/{dbname}")
        except KeyError as e:
            logger.error(f"Missing required configuration: {e}")
            raise

    def _setup_engine_and_session(self):
        """
        Sets up the SQLAlchemy engine and session factory.

        Raises:
        Exception: If there is an error in setting up the engine and session.
        """
        try:
            self.engine = create_engine(self.DATABASE_URL, pool_size=10, max_overflow=20)
            self.SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
            self.Base = Base
            logger.info("Engine and session setup successfully.")
        except Exception as e:
            logger.error(f"Error setting up engine and session: {e}")
            raise

    def _check_database_existence(self):
        """
        Checks if the database is accessible by executing a simple query.

        Raises:
        ConnectionError: If the database is not accessible.
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                if result.scalar() == 1:
                    logger.info("Database is accessible.")
                else:
                    logger.error("Database is not accessible.")
                    raise ConnectionError("Database is not accessible.")
        except Exception as e:
            logger.error(f"Error checking database existence: {e}")
            raise

    def init_db(self):
        """
        Initializes the database by creating all tables defined in the models.

        Raises:
        Exception: If there is an error in initializing the database.
        """
        try:
            from models.file import File
            from models.folder import Folder
            self.Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully.")
        except Exception as e:
            logger.error(f"Error initializing the database: {e}")
            raise

    def get_db_session(self):
        """
        Starts a new database session.

        Returns:
        Session: A new SQLAlchemy session.
        """
        session = self.SessionLocal()
        logger.info("Database session started.")
        return session

    def close_db_session(self, session):
        """
        Closes the provided database session.

        Parameters:
        session (Session): The SQLAlchemy session to close.

        Raises:
        Exception: If there is an error in closing the session.
        """
        try:
            session.close()
            self.SessionLocal.remove()
            logger.info("Database session closed.")
        except Exception as e:
            logger.error(f"Error closing database session: {e}")
            raise
