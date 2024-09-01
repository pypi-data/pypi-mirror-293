import logging

try:
    import aiosqlite

except ImportError:
    raise ImportError('To use sqlite storage you need to install aiosqlite: `pip install aiosqlite`')

from proxy_messages_aiogram.storages import types
from proxy_messages_aiogram.storages.base import BaseStorage

logger = logging.getLogger('proxy_messages_aiogram')


class SQLiteStorage(BaseStorage):
    db_path: str
    db_connection: aiosqlite.Connection

    def __init__(self, db_path: str = 'db.sqlite3') -> None:
        self.db_path = db_path

    async def _setup_database(self):
        await self.db_connection.execute(
            """
            CREATE TABLE IF NOT EXISTS proxy_message_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_id INTEGER,
                original_chat_hash TEXT,
                target_chat_topic_id INTEGER,
                target_chat_id INTEGER,
                original_chat_id INTEGER,
                original_chat_topic_id INTEGER
            )
        """
        )
        await self.db_connection.commit()

    async def on_startup(self):
        self.db_connection = await aiosqlite.connect(self.db_path)
        self.db_connection.row_factory = aiosqlite.Row

        await self._setup_database()

        logger.info('Testing connection to SQLite database')
        async with self.db_connection.execute('SELECT name FROM sqlite_master WHERE type="table"') as cursor:
            tables = await cursor.fetchall()
            logger.info(f'SQLite is connected. Tables: {[table[0] for table in tables]}')

    async def on_shutdown(self):
        if self.db_connection:
            await self.db_connection.close()

    async def set_proxy_message_info(
        self,
        bot_id: int,
        proxy_message_info: types.ProxyMessageInfo,
    ):
        await self.db_connection.execute(
            """
            INSERT OR REPLACE INTO proxy_message_info (
                bot_id, original_chat_hash, target_chat_topic_id,
                target_chat_id, original_chat_id, original_chat_topic_id
            ) VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                bot_id,
                proxy_message_info.original_chat_hash,
                proxy_message_info.target_chat_topic_id,
                proxy_message_info.target_chat_id,
                proxy_message_info.original_chat_id,
                proxy_message_info.original_chat_topic_id,
            ),
        )
        await self.db_connection.commit()

    async def get_proxy_message_info__by__original_chat_hash(
        self,
        bot_id: int,
        original_chat_hash: str,
    ) -> types.ProxyMessageInfo | None:
        async with self.db_connection.execute(
            """
            SELECT bot_id, target_chat_id, target_chat_topic_id, original_chat_id, original_chat_topic_id
            FROM proxy_message_info
            WHERE bot_id = ? AND original_chat_hash = ?
        """,
            (bot_id, original_chat_hash),
        ) as cursor:
            row = await cursor.fetchone()

        if row is None:
            return None

        return types.ProxyMessageInfo.model_validate(dict(row))

    async def get_proxy_message_info__by__target_chat_topic_id(
        self,
        bot_id: int,
        target_chat_topic_id: int,
    ) -> types.ProxyMessageInfo | None:
        async with self.db_connection.execute(
            """
            SELECT bot_id, original_chat_hash, target_chat_id, target_chat_topic_id, original_chat_id, original_chat_topic_id
            FROM proxy_message_info
            WHERE bot_id = ? AND target_chat_topic_id = ?
        """,
            (bot_id, target_chat_topic_id),
        ) as cursor:
            row = await cursor.fetchone()

        if row is None:
            return None

        return types.ProxyMessageInfo.model_validate(dict(row))
