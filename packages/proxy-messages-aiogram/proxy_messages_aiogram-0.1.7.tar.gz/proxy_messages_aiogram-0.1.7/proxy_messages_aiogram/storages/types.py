import aiogram
from pydantic import BaseModel

from proxy_messages_aiogram.utils import generate_unique_hash


class ProxyMessageInfo(BaseModel):
    bot_id: int
    target_chat_id: int | None
    target_chat_topic_id: int | None
    original_chat_id: int
    original_chat_topic_id: int | None

    @property
    def original_chat_hash(self) -> str:
        return generate_unique_hash([self.original_chat_id, self.original_chat_topic_id])

    @classmethod
    def from_message(
        cls,
        message: aiogram.types.Message,
        target_chat_id: int | None = None,
        target_chat_topic_id: int | None = None,
    ):
        return cls(
            bot_id=message.bot.id,
            target_chat_id=target_chat_id,
            target_chat_topic_id=target_chat_topic_id,
            original_chat_id=message.chat.id,
            original_chat_topic_id=message.message_thread_id,
        )

    @classmethod
    def cls_original_chat_hash(cls, message: aiogram.types.Message) -> str:
        return cls.from_message(message).original_chat_hash
