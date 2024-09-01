# Proxy Messages for Aiogram

A library implementing a simple way to proxy messages from a bot to a selected channel-forum

[![PyPI](https://img.shields.io/pypi/v/proxy-messages-aiogram)](https://pypi.org/project/proxy-messages-aiogram/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/proxy-messages-aiogram)](https://pypi.org/project/proxy-messages-aiogram/)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/proxy-messages-aiogram)](https://gitlab.com/rocshers/python/proxy-messages-aiogram)
[![Docs](https://img.shields.io/badge/docs-exist-blue)](https://rocshers.gitlab.io/python/proxy-messages-aiogram/)

[![Test coverage](https://codecov.io/gitlab/rocshers:python/proxy-messages-aiogram/graph/badge.svg?token=3C6SLDPHUC)](https://codecov.io/gitlab/rocshers:python/proxy-messages-aiogram)
[![Downloads](https://static.pepy.tech/badge/proxy-messages-aiogram)](https://pepy.tech/project/proxy-messages-aiogram)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/proxy-messages-aiogram)](https://gitlab.com/rocshers/python/proxy-messages-aiogram)

## Functionality

## Installation

`pip install proxy-messages-aiogram`

## Quick start

Mode details in [example](./test_app.py).

```python
from aiogram import Bot, Dispatcher

from proxy_messages_aiogram.proxy_managers import ProxyManager
from proxy_messages_aiogram.storages.sqlite_storage import SQLiteStorage

dp = Dispatcher()

proxy_manager = ProxyManager(
    SQLiteStorage(),
    {TARGET_TG_CHAT_ID},
)

@dp.message(proxy_manager.proxy_magic_filter)
async def proxy_messages_handler(message: Message) -> None:
    await proxy_manager.proxy(message)


@dp.message(proxy_manager.answer_magic_filter)
async def answer_messages_handler(message: Message) -> None:
    await proxy_manager.answer(message)
```

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/proxy-messages-aiogram/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/proxy-messages-aiogram>

Before adding changes:

```bash
make install-dev
```

After changes:

```bash
make format test
```
