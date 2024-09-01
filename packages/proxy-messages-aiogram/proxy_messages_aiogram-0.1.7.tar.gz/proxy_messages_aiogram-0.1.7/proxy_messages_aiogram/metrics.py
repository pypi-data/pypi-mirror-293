import logging

logger = logging.getLogger('proxy_messages_aiogram')

try:
    import prometheus_client as pc

except ImportError:
    logger.warning('ImportError(prometheus_client). Collecting metrics from the "proxy_messages_aiogram" is disabled.')

    from unittest.mock import MagicMock

    pc = MagicMock()

PREFIX = 'proxy_messages_aiogram'

m_messages_proxied = pc.Counter(  # type: ignore
    f'{PREFIX}_messages_proxied',
    'Count of proxied messaged from original chat to target chat',
    ['bot', 'original_chat_id'],
)
m_messages_proxying_time = pc.Histogram(  # type: ignore
    f'{PREFIX}_messages_proxying_time',
    'Tine proxying messaged from original chat to target chat',
    ['bot'],
)


m_messages_answered = pc.Counter(  # type: ignore
    f'{PREFIX}_messages_answered',
    'Count of proxied messaged from target chat to original chat',
    ['bot', 'original_chat_id', 'error'],
)

m_messages_answering_time = pc.Histogram(  # type: ignore
    f'{PREFIX}_messages_answering_time',
    'Count of proxied messaged from target chat to original chat',
    ['bot'],
)
