from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TelegramConfig:
    bot_token: str


@dataclass(frozen=True)
class ChannelsConfig:
    telegram: TelegramConfig


def _load_dotenv(dotenv_path: Path) -> None:
    """
    Мини-реализация dotenv: читает KEY=VALUE, игнорирует пустые строки и #комменты.
    Ничего не перетирает, если переменная уже есть в окружении.
    """
    if not dotenv_path.exists():
        return

    for raw in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        os.environ.setdefault(key, value)


def _require(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing required env var: {name}")
    return val


def load_channels_config() -> ChannelsConfig:
    here = Path(__file__).resolve().parent
    _load_dotenv(here / ".env")

    telegram = TelegramConfig(
        bot_token=_require("TELEGRAM_BOT_TOKEN"),
    )
    return ChannelsConfig(telegram=telegram)