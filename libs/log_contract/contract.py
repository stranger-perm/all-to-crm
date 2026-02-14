from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from typing import Any, Dict, Optional

# Поля, которые мы считаем "системным контекстом"
CTX_KEYS = (
    "trace_id",
    "dump_id",
    "source",
    "stage",
    "connector",
    "action",
)

# Поля LogRecord, которые не надо утаскивать в extra-json
_RESERVED_RECORD_KEYS = {
    "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
    "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
    "created", "msecs", "relativeCreated", "thread", "threadName",
    "processName", "process",
}

def make_trace_id() -> str:
    # короткий, но достаточно уникальный для корреляции
    return secrets.token_hex(8)  # 16 hex chars

def utc_ts() -> str:
    # 2026-02-13T12:34:56.789Z
    dt = datetime.now(timezone.utc)
    return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")

def sanitize_extra(extra: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not extra:
        return {}
    out: Dict[str, Any] = {}
    for k, v in extra.items():
        if k in _RESERVED_RECORD_KEYS:
            continue
        # JSON-safe: всё, что не сериализуется — в строку
        try:
            json.dumps(v)
            out[k] = v
        except Exception:
            out[k] = str(v)
    return out

def format_tsv(
    *,
    ts: str,
    level: str,
    logger_name: str,
    message: str,
    extra: Dict[str, Any],
    exc_text: Optional[str] = None,
) -> str:
    extra_json = json.dumps(extra, ensure_ascii=False, separators=(",", ":"))
    if exc_text:
        return f"{ts}\t{level}\t{logger_name}\t{message}\t{extra_json}\t{exc_text}"
    return f"{ts}\t{level}\t{logger_name}\t{message}\t{extra_json}"