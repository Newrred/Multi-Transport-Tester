from __future__ import annotations

from typing import Any, Dict, List, Optional

import tkinter as tk
from tkinter import ttk

from engine import AppCfg, RedisCfg
from ui_widgets import CollapsibleSection

from .base import SafeFloatFn, SafeIntFn


class RedisTransportUI:
    name = "redis"

    def __init__(self, master: tk.Misc):
        self._master = master

        # top vars
        self.host = tk.StringVar(master, value="127.0.0.1")
        self.port = tk.StringVar(master, value="6379")
        self.db = tk.StringVar(master, value="0")

        # settings vars
        self.password = tk.StringVar(master, value="")
        self.pub_channel = tk.StringVar(master, value="tcp_test_pub")
        self.sub_channels = tk.StringVar(master, value="tcp_test_sub")

        # UI refs
        self.top_frame: Optional[ttk.Frame] = None
        self.settings_frame: Optional[ttk.Frame] = None

        self.ent_host: Optional[ttk.Entry] = None
        self.ent_port: Optional[ttk.Entry] = None
        self.ent_db: Optional[ttk.Entry] = None

        self.ent_password: Optional[ttk.Entry] = None
        self.ent_pub: Optional[ttk.Entry] = None
        self.ent_sub: Optional[ttk.Entry] = None

        self.lock_widgets: List[tk.Misc] = []

    def build_top(self, parent: ttk.Frame) -> None:
        fr = ttk.Frame(parent)
        self.top_frame = fr

        ttk.Label(fr, text="Host").pack(side="left")
        self.ent_host = ttk.Entry(fr, textvariable=self.host, width=18)
        self.ent_host.pack(side="left", padx=(6, 4))

        ttk.Label(fr, text=":").pack(side="left")
        self.ent_port = ttk.Entry(fr, textvariable=self.port, width=8)
        self.ent_port.pack(side="left", padx=(4, 10))

        ttk.Label(fr, text="DB").pack(side="left")
        self.ent_db = ttk.Entry(fr, textvariable=self.db, width=6)
        self.ent_db.pack(side="left", padx=(6, 0))

        self.lock_widgets.extend([w for w in [self.ent_host, self.ent_port, self.ent_db] if w is not None])

    def build_settings(self, parent: ttk.Frame) -> None:
        fr = ttk.Frame(parent)
        self.settings_frame = fr

        sec = CollapsibleSection(fr, "Redis Settings", expanded=True)
        sec.pack(fill="x", pady=6)
        box = sec.content
        box.grid_columnconfigure(1, weight=1)

        label_w = 20
        ttk.Label(box, text="Password", width=label_w, anchor="w").grid(row=0, column=0, sticky="w", padx=6, pady=3)
        self.ent_password = ttk.Entry(box, textvariable=self.password, width=20, show="*")
        self.ent_password.grid(row=0, column=1, sticky="w", padx=6, pady=3)

        ttk.Label(box, text="PUB Channel", width=label_w, anchor="w").grid(row=1, column=0, sticky="w", padx=6, pady=3)
        self.ent_pub = ttk.Entry(box, textvariable=self.pub_channel)
        self.ent_pub.grid(row=1, column=1, sticky="ew", padx=6, pady=3)

        ttk.Label(box, text="SUB Channels (comma)", width=label_w, anchor="w").grid(row=2, column=0, sticky="w", padx=6, pady=3)
        self.ent_sub = ttk.Entry(box, textvariable=self.sub_channels)
        self.ent_sub.grid(row=2, column=1, sticky="ew", padx=6, pady=(3, 6))

        self.lock_widgets.extend([w for w in [self.ent_password, self.ent_pub, self.ent_sub] if w is not None])

    def fill_cfg(self, cfg: AppCfg, safe_int: SafeIntFn, safe_float: SafeFloatFn) -> None:
        sub = [c.strip() for c in self.sub_channels.get().split(",") if c.strip()]
        cfg.redis = RedisCfg(
            enabled=True,
            host=self.host.get().strip() or "127.0.0.1",
            port=safe_int(self.port.get(), 6379, "Redis port", 1, 65535),
            db=safe_int(self.db.get(), 0, "Redis db", 0, 999999),
            password=self.password.get(),
            pub_channel=self.pub_channel.get().strip() or "tcp_test_pub",
            sub_channels=sub or ["tcp_test_sub"],
        )

    def can_send(self, stats: Dict[str, Any]) -> bool:
        transport = (stats.get("transport") or "-").lower()
        state = (stats.get("state") or "idle").lower()
        return transport == "redis" and state == "connected"

    def apply_runtime_state(self, stats: Dict[str, Any]) -> None:
        return

    def apply_tk_colors(self, palette: Dict[str, str]) -> None:
        return
