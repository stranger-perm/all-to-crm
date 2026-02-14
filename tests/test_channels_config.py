from __future__ import annotations

from pathlib import Path

import libs.channels.config as cfgmod


def test_load_channels_config_reads_dotenv_next_to_config(monkeypatch, tmp_path: Path) -> None:
    # 1) Подменяем __file__ модуля, чтобы config.py "думал",
    #    что лежит в tmp папке (и искал .env там же).
    fake_module_dir = tmp_path / "channels"
    fake_module_dir.mkdir(parents=True, exist_ok=True)

    # 2) Создаём .env рядом с "модулем".
    (fake_module_dir / ".env").write_text(
        "TELEGRAM_BOT_TOKEN='from_dotenv'\n",
        encoding="utf-8",
    )

    # 3) Убираем влияние реального окружения (чистый тест).
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)

    # 4) Подсовываем модулю "левый" путь до файла.
    monkeypatch.setattr(cfgmod, "__file__", str(fake_module_dir / "config.py"), raising=False)

    # 5) Вызываем код под тестом.
    cfg = cfgmod.load_channels_config()

    # 6) Проверяем, что токен считан из .env и упакован в объект.
    assert cfg.telegram.bot_token == "from_dotenv"