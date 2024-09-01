import logging

import aiogram
import aiogram.exceptions
from aiogram import F, MagicFilter
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message

from proxy_messages_aiogram import metrics, texts
from proxy_messages_aiogram.storages import types
from proxy_messages_aiogram.storages.base import BaseStorage

logger = logging.getLogger('proxy_messages_aiogram')


class ProxyMessagesManager(object):
    def __init__(self, storage: BaseStorage, target_chat_id: int, message: Message) -> None:
        self.storage = storage
        self.target_chat_id = target_chat_id
        self.message = message
        self.bot = message.bot
        self.bot_info = message.bot._me

    @property
    def topic_name(self):
        if self.message.message_thread_id is not None:
            return f'{self.message.chat.full_name} -> {self.message.message_thread_id} [by {self.bot._me.username}]'

        return f'{self.message.chat.full_name} [by {self.bot._me.username}]'

    async def send_chat_info_message(self, target_chat_topic_id: int):
        text_data = {
            'original_user_id': self.message.from_user.id,
            'original_user_username': self.message.from_user.username,
            'original_user_name': self.message.from_user.full_name,
            'original_chat_id': self.message.chat.id,
            'original_chat_username': self.message.chat.username,
            'original_chat_name': self.message.chat.full_name,
            'original_chat_is_group': self.message.chat.id != self.message.from_user.id,
            'original_chat_is_forum': bool(self.message.chat.is_forum),
            'original_chat_topic_id': self.message.message_thread_id,
            'bot_id': self.bot.id,
            'bot_username': self.bot._me.username,
            'bot_name': self.bot._me.full_name,
            'chat_topic_id': target_chat_topic_id,
            'chat_topic_name': self.topic_name,
        }

        text = texts.NEW_TOPIC_INFO_1.format(**text_data)

        message = await self.bot.send_message(
            self.target_chat_id,
            text,
            message_thread_id=target_chat_topic_id,
            parse_mode=ParseMode.HTML,
        )
        await self.bot.pin_chat_message(self.target_chat_id, message.message_id, disable_notification=False)

    async def create_new_topic(self):
        target_chat_topic = await self.bot.create_forum_topic(self.target_chat_id, self.topic_name)
        target_chat_topic_id = target_chat_topic.message_thread_id
        await self.send_chat_info_message(target_chat_topic_id)

        return target_chat_topic_id

    async def init_new_topic(self) -> types.ProxyMessageInfo:
        proxy_message_info = types.ProxyMessageInfo.from_message(self.message, self.target_chat_id)

        proxy_message_info.target_chat_topic_id = await self.create_new_topic()
        await self.storage.set_proxy_message_info(self.bot.id, proxy_message_info)

        return proxy_message_info

    async def proxy(self):
        if self.bot_info is None:
            self.bot_info = await self.bot.me()

        proxy_message_info = await self.storage.get_proxy_message_info__by__original_chat_hash(
            self.bot.id,
            types.ProxyMessageInfo.cls_original_chat_hash(self.message),
        )

        if proxy_message_info is None:
            proxy_message_info = await self.init_new_topic()

        try:
            await self.message.copy_to(self.target_chat_id, proxy_message_info.target_chat_topic_id)

        except aiogram.exceptions.TelegramBadRequest as ex:
            # TelegramBadRequest: Telegram server says - Bad Request: message thread not found
            logger.exception(ex)
            proxy_message_info = await self.init_new_topic()
            await self.message.copy_to(self.target_chat_id, proxy_message_info.target_chat_topic_id)


class AnswerMessagesManager(object):
    def __init__(self, storage: BaseStorage, target_chat_id: int, message: Message) -> None:
        self.storage = storage
        self.target_chat_id = target_chat_id
        self.message = message
        self.bot = message.bot

        assert self.bot is not None

    async def proxy(self) -> tuple[types.ProxyMessageInfo | None, BaseException | None]:
        assert self.message.message_thread_id is not None

        proxy_message_info = await self.storage.get_proxy_message_info__by__target_chat_topic_id(
            self.bot.id,
            self.message.message_thread_id,
        )

        if proxy_message_info is None:
            logger.warning(
                'We can`t find original chat for [{} / {} / {}]'.format(
                    self.bot.id,
                    self.message.message_id,
                    self.message.message_thread_id,
                )
            )
            return None, None

        try:
            await self.message.copy_to(
                proxy_message_info.original_chat_id,
                proxy_message_info.original_chat_topic_id,
            )

        except BaseException as ex:
            logger.exception(ex)
            await self.message.reply(f'We can`t proxy this message [{self.message.message_id}]; Error: {ex}')
            return proxy_message_info, ex

        return proxy_message_info, None


class ProxyManager(object):
    PROXY_MESSAGES_MANAGER_TYPE: type[ProxyMessagesManager] = ProxyMessagesManager
    ANSWER_MESSAGES_MANAGER_TYPE: type[AnswerMessagesManager] = AnswerMessagesManager

    def __init__(self, storage: BaseStorage, target_chat_id: int) -> None:
        self.storage = storage
        self.target_chat_id = target_chat_id

    async def on_startup(self):
        await self.storage.on_startup()

    async def on_shutdown(self):
        await self.storage.on_shutdown()

    @property
    def proxy_magic_filter(self) -> MagicFilter:
        return F.chat.id != self.target_chat_id

    @property
    def answer_magic_filter(self) -> MagicFilter:
        return (F.chat.id == self.target_chat_id) & (F.from_user.is_bot == False) & F.message_thread_id

    async def proxy(self, message: Message):
        logger.info(f'Proxing message from original chat [{message.chat.id}] to target chat [{self.target_chat_id}]')

        with metrics.m_messages_proxying_time.labels(message.bot.id).time():
            proxy_messages_manager = self.PROXY_MESSAGES_MANAGER_TYPE(self.storage, self.target_chat_id, message)
            await proxy_messages_manager.proxy()

        metrics.m_messages_proxied.labels(message.bot.id, message.chat.id).inc()

    async def answer(self, message: Message):
        logger.info(
            f'Proxing message from target chat [{message.chat.id}/{message.message_thread_id}] to original chat'
        )

        with metrics.m_messages_answering_time.labels(message.bot.id).time():
            proxy_messages_manager = self.ANSWER_MESSAGES_MANAGER_TYPE(self.storage, self.target_chat_id, message)
            proxy_message_info, ex = await proxy_messages_manager.proxy()

        if proxy_message_info is None:
            metrics.m_messages_answered.labels(message.bot.id, 'None', 'None').inc()

        elif ex is None:
            metrics.m_messages_answered.labels(message.bot.id, proxy_message_info.original_chat_id, 'None').inc()

        else:
            metrics.m_messages_answered.labels(message.bot.id, proxy_message_info.original_chat_id, str(type(ex))).inc()
