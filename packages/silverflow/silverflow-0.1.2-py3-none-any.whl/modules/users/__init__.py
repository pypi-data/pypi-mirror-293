import abc

from silverriver.interfaces.data_models import ChatMessage


class BaseUser(abc.ABC):
    @abc.abstractmethod
    def send_message(self, message: str) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_unread_messages(self, limit: int = 10, offset: int = 0) -> list[ChatMessage]:
        raise NotImplementedError

    @abc.abstractmethod
    def mark_messages_read(self, message_ids: list[int]) -> dict:
        raise NotImplementedError
