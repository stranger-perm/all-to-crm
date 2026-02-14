# libs/channels/telegram.py
from __future__ import annotations

from typing import Optional, Union

import httpx

from .config import TelegramConfig  # <-- вот это важно

ChatId = Union[int, str]


class TelegramSendError(RuntimeError):
    """Raised when Telegram API call fails or returns ok=false."""


class TelegramDriver:
    def __init__(self, config: TelegramConfig, *, timeout_s: float = 10.0) -> None:
        self._token = config.bot_token
        self._timeout = timeout_s

    def send(self, chat_id: ChatId, message: str, *, silent: Optional[bool] = None) -> None:
        if chat_id is None or (isinstance(chat_id, str) and not chat_id.strip()):
            raise ValueError("chat_id is required")
        if message is None or (isinstance(message, str) and not message.strip()):
            raise ValueError("message is required")

        url = f"https://api.telegram.org/bot{self._token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}

        if silent is not None:
            payload["disable_notification"] = bool(silent)

        try:
            resp = httpx.post(url, json=payload, timeout=self._timeout)
        except httpx.HTTPError as e:
            raise TelegramSendError(f"Telegram request failed: {type(e).__name__}: {e}") from e

        if resp.status_code >= 400:
            raise TelegramSendError(f"Telegram HTTP error: {resp.status_code} {resp.reason_phrase}")

        try:
            data = resp.json()
        except ValueError as e:
            raise TelegramSendError("Telegram returned non-JSON response") from e

        if not isinstance(data, dict) or data.get("ok") is not True:
            desc = str(data.get("description") or "") if isinstance(data, dict) else ""
            raise TelegramSendError(f"Telegram API error: {desc or 'ok=false'}")