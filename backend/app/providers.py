from __future__ import annotations

import os


class NasdaqProvider:
    def __init__(self) -> None:
        self.enabled = bool(os.getenv("NASDAQ_API_KEY"))
        self.provider = "nasdaq-mock" if not self.enabled else "nasdaq-live"

    def quota(self) -> dict:
        if self.enabled:
            used = 128
            limit = 1000
        else:
            used = 0
            limit = 100
        status = "ok" if used / limit < 0.8 else "warning"
        return {
            "provider": self.provider,
            "used": used,
            "limit": limit,
            "status": status,
        }
