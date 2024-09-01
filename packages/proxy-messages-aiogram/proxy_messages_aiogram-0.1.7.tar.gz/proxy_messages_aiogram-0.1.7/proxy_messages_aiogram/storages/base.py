import abc

from proxy_messages_aiogram.storages import types


class BaseStorage(abc.ABC):
    def __init__(self) -> None:
        pass

    async def on_startup(self):
        pass

    async def on_shutdown(self):
        pass

    @abc.abstractmethod
    async def set_proxy_message_info(
        self,
        bot_id: int,
        proxy_message_info: types.ProxyMessageInfo,
    ):
        pass

    @abc.abstractmethod
    async def get_proxy_message_info__by__original_chat_hash(
        self,
        bot_id: int,
        original_chat_hash: str,
    ) -> types.ProxyMessageInfo | None:
        pass

    @abc.abstractmethod
    async def get_proxy_message_info__by__target_chat_topic_id(
        self,
        bot_id: int,
        target_chat_topic_id: int,
    ) -> types.ProxyMessageInfo | None:
        pass
