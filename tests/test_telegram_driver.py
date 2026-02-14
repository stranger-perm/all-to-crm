from __future__ import annotations

import libs.channels.telegram as tgmod
from libs.channels.config import TelegramConfig


def test_telegram_driver_does_not_send_disable_notification_when_silent_is_none(monkeypatch) -> None:
    # Сюда мы сохраним то, что драйвер реально отправил в httpx.post(...)
    captured: dict = {}

    class FakeResponse:
        status_code = 200
        reason_phrase = "OK"

        def json(self):
            return {"ok": True}

    def fake_post(url, json, timeout):
        captured["url"] = url
        captured["json"] = json
        captured["timeout"] = timeout
        return FakeResponse()

    # Подменяем tgmod.httpx.post на нашу фейковую функцию
    monkeypatch.setattr(tgmod.httpx, "post", fake_post)

    driver = tgmod.TelegramDriver(TelegramConfig(bot_token="TOKEN"), timeout_s=1.0)
    driver.send(chat_id=472907090, message="Тест", silent=None)

    # Главное: параметр disable_notification НЕ должен появиться,
    # если silent не передан (None).
    assert "disable_notification" not in captured["json"]

    # И базовые поля должны быть
    assert captured["json"]["chat_id"] == 472907090
    assert captured["json"]["text"] == "Тест"