from __future__ import annotations

import libs.channels.bootstrap as boot


def test_create_send_telegram_proxies_call_to_driver(monkeypatch) -> None:
    calls = []

    # 1) Подменяем загрузчик конфига, чтобы не трогать .env / env
    class FakeTelegramCfg:
        bot_token = "TOKEN"

    class FakeChannelsCfg:
        telegram = FakeTelegramCfg()

    monkeypatch.setattr(boot, "load_channels_config", lambda: FakeChannelsCfg())

    # 2) Подменяем TelegramDriver на фейковый, чтобы не трогать httpx
    class FakeDriver:
        def __init__(self, config, *, timeout_s=10.0):
            self.config = config
            self.timeout_s = timeout_s

        def send(self, *, chat_id, message, silent=None):
            calls.append((chat_id, message, silent))

    monkeypatch.setattr(boot, "TelegramDriver", FakeDriver)

    # 3) Получаем функцию из фабрики и вызываем
    send = boot.create_send_telegram()
    send(472907090, "Тест", True)

    # 4) Проверяем, что фабрика/витрина прокинула параметры 1-в-1
    assert calls == [(472907090, "Тест", True)]