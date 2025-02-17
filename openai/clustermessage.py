from abc import abstractmethod, ABC

class ClusterMessage(ABC):
    """Base class for cluster messages."""

    @abstractmethod
    def process_message(self) -> str:
        """Returns the type of the message."""
        pass

    @abstractmethod
    def send_message(self) -> str:
        """Returns the content of the message."""
        pass