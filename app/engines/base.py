from abc import ABC, abstractmethod

class BaseEngine(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def test_connection(self) -> bool:
        """Attempt to connect to the DB and return True if
        successful, False otherwise."""
        pass

    @abstractmethod
    def backup(self, destination_path: str):
        """Execute the backup logic."""
        pass