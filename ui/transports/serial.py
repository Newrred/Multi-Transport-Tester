from __future__ import annotations

from typing import Any, Dict, Optional

import tkinter as tk
from tkinter import ttk

from engine import AppCfg, SerialCfg
from ui_widgets import CollapsibleSection

from .base import SafeFloatFn, SafeIntFn


class SerialTransportUI:
    name = "serial"

    def __init__(self, master: tk.Misc):
        self._master = master

        # top vars
        self.port = tk.StringVar(master, value="COM3")
        self.baud = tk.StringVar(master, value="115200")

        # settings vars
        self.timeout = tk.StringVar(master, value="0.2")
        self.write_timeout = tk.StringVar(master, value="1.0")

        # UI refs
        self.top_frame: Optional[ttk.Frame] = None
        self.settings_frame: Optional[ttk.Frame] = None

        self.ent_port: Optional[ttk.Entry] = None
        self.ent_baud: Optional[ttk.Entry] = None
        self.ent_timeout: Optional[ttk.Entry] = None
        self.ent_write_timeout: Optional[ttk.Entry] = None

        self.lock_widgets: list[tk.Misc] = []

    def build_top(self, parent: ttk.Frame) -> None:
        fr = ttk.Frame(parent)
        self.top_frame = fr

        ttk.Label(fr, text="Port").pack(side="left")
        self.ent_port = ttk.Entry(fr, textvariable=self.port, width=18)
        self.ent_port.pack(side="left", padx=(6, 10))

        ttk.Label(fr, text="Baud").pack(side="left")
        self.ent_baud = ttk.Entry(fr, textvariable=self.baud, width=10)
        self.ent_baud.pack(side="left", padx=(6, 0))

        self.lock_widgets.extend([w for w in [self.ent_port, self.ent_baud] if w is not None])

    def build_settings(self, parent: ttk.Frame) -> None:
        fr = ttk.Frame(parent)
        self.settings_frame = fr

        sec = CollapsibleSection(fr, "Serial Settings", expanded=True)
        sec.pack(fill="x", pady=6)
        box = sec.content
        box.grid_columnconfigure(1, weight=1)

        ttk.Label(box, text="Read Timeout (s)", width=18, anchor="w").grid(row=0, column=0, sticky="w", padx=6, pady=3)
        self.ent_timeout = ttk.Entry(box, textvariable=self.timeout, width=12)
        self.ent_timeout.grid(row=0, column=1, sticky="w", padx=6, pady=3)

        ttk.Label(box, text="Write Timeout (s)", width=18, anchor="w").grid(row=1, column=0, sticky="w", padx=6, pady=3)
        self.ent_write_timeout = ttk.Entry(box, textvariable=self.write_timeout, width=12)
        self.ent_write_timeout.grid(row=1, column=1, sticky="w", padx=6, pady=(3, 6))

        self.lock_widgets.extend([w for w in [self.ent_timeout, self.ent_write_timeout] if w is not None])

    def fill_cfg(self, cfg: AppCfg, safe_int: SafeIntFn, safe_float: SafeFloatFn) -> None:
        cfg.serial = SerialCfg(
            enabled=True,
            port=self.port.get().strip() or "COM3",
            baudrate=safe_int(self.baud.get(), 115200, "Serial baud", 300, 20_000_000),
            timeout_sec=safe_float(self.timeout.get(), 0.2, "Serial timeout", 0.0, 10.0),
            write_timeout_sec=safe_float(self.write_timeout.get(), 1.0, "Serial write timeout", 0.0, 60.0),
        )

    def can_send(self, stats: Dict[str, Any]) -> bool:
        transport = (stats.get("transport") or "-").lower()
        state = (stats.get("state") or "idle").lower()
        return transport == "serial" and state == "connected"

    def apply_runtime_state(self, stats: Dict[str, Any]) -> None:
        return

    def apply_tk_colors(self, palette: Dict[str, str]) -> None:
        return
