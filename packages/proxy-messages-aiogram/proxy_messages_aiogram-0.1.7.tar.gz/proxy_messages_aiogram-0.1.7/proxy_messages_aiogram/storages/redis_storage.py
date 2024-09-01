import logging

try:
    import redis.asyncio as redis

except ImportError:
    raise ImportError('To use redis storage you need to install redis: `pip install redis`')


from proxy_messages_aiogram.storages import types
from proxy_messages_aiogram.storages.base import BaseStorage

logger = logging.getLogger('proxy_messages_aiogram')


class RedisStorage(BaseStorage):
    def __init__(self, *args, **kwargs) -> None:
        self.client = redis.Redis(*args, **kwargs)

    async def on_startup(self):
        logger.info('Testing connection to redis')
        redis_info = await self.client.info()
        redis_version = redis_info['redis_version']
        logger.info(f'Redis is connected. Version: {redis_version}')

    async def on_shutdown(self):
        await self.client.close()

    async def set_proxy_message_info(
        self,
        bot_id: int,
        proxy_message_info: types.ProxyMessageInfo,
    ):
        await self.client.hset(
            f'proxy_message_info__by__original_chat_hash:{bot_id}',
            proxy_message_info.original_chat_hash,
            proxy_message_info.json(),
        )
        await self.client.hset(
            f'proxy_message_info__by__target_chat_topic_id:{bot_id}',
            proxy_message_info.target_chat_topic_id,
            proxy_message_info.json(),
        )

    async def get_proxy_message_info__by__original_chat_hash(
        self,
        bot_id: int,
        original_chat_hash: str,
    ) -> types.ProxyMessageInfo | None:
        proxy_message_info_json = await self.client.hget(
            f'proxy_message_info__by__original_chat_hash:{bot_id}',
            original_chat_hash,
        )

        if proxy_message_info_json is None:
            return None

        return types.ProxyMessageInfo.model_validate_json(proxy_message_info_json)

    async def get_proxy_message_info__by__target_chat_topic_id(
        self,
        bot_id: int,
        target_chat_topic_id: int,
    ) -> types.ProxyMessageInfo | None:
        proxy_message_info_json = await self.client.hget(
            f'proxy_message_info__by__target_chat_topic_id:{bot_id}',
            target_chat_topic_id,
        )

        if proxy_message_info_json is None:
            return None

        return types.ProxyMessageInfo.model_validate_json(proxy_message_info_json)
