from __future__ import annotations

from typing import Optional, Union, Callable

from .config import load_channels_config
from .telegram import TelegramDriver

ChatId = Union[int, str]
SendTelegramFn = Callable[[ChatId, str, Optional[bool]], None]


def create_send_telegram() -> SendTelegramFn:
    cfg = load_channels_config()
    driver = TelegramDriver(cfg.telegram)

    def send_telegram(chat_id: ChatId, message: str, silent: Optional[bool] = None) -> None:
        driver.send(chat_id=chat_id, message=message, silent=silent)

    return send_telegram