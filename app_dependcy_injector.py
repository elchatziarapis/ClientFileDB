from injector import Module, provider, singleton
from database import Database
from services.folder_service import FolderService
from controllers.folder_controller import FolderController

class AppInjector(Module):
    """Module for providing dependencies."""

    @singleton
    @provider
    def provide_database(self) -> Database:
        """Provides a singleton instance of Database."""
        return Database()

    @singleton
    @provider
    def provide_folder_service(self, db: Database) -> FolderService:
        """Provides a singleton instance of FolderService."""
        return FolderService(db)

    @singleton
    @provider
    def provide_folder_controller(self, folder_service: FolderService) -> FolderController:
        """Provides a singleton instance of FolderController."""
        return FolderController(folder_service)
