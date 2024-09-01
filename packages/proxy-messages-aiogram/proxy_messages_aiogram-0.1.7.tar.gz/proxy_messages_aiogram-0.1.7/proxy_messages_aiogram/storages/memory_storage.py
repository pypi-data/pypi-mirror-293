import logging

from proxy_messages_aiogram.storages import types
from proxy_messages_aiogram.storages.base import BaseStorage

logger = logging.getLogger('proxy_messages_aiogram')


class MemoryStorage(BaseStorage):
    memory_dict: dict[tuple[int, str | int], types.ProxyMessageInfo]

    def __init__(self) -> None:
        self.memory_dict = {}

    async def set_proxy_message_info(
        self,
        bot_id: int,
        proxy_message_info: types.ProxyMessageInfo,
    ):
        self.memory_dict[(bot_id, proxy_message_info.original_chat_hash)] = proxy_message_info
        self.memory_dict[(bot_id, proxy_message_info.target_chat_topic_id)] = proxy_message_info

    async def get_proxy_message_info__by__original_chat_hash(
        self,
        bot_id: int,
        original_chat_hash: str,
    ) -> types.ProxyMessageInfo | None:
        return self.memory_dict.get((bot_id, original_chat_hash))

    async def get_proxy_message_info__by__target_chat_topic_id(
        self,
        bot_id: int,
        target_chat_topic_id: int,
    ) -> types.ProxyMessageInfo | None:
        return self.memory_dict.get((bot_id, target_chat_topic_id))
