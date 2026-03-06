from __future__ import annotations

from typing import Any, Dict, Optional

import tkinter as tk
from tkinter import ttk

from engine import AppCfg, UdpCfg
from ui_widgets import CollapsibleSection

from .base import SafeFloatFn, SafeIntFn


class UdpTransportUI:
    name = "udp"

    def __init__(self, master: tk.Misc):
        self._master = master

        # vars
        self.bind_host = tk.StringVar(master, value="0.0.0.0")
        self.bind_port = tk.StringVar(master, value="7001")
        self.target_host = tk.StringVar(master, value="127.0.0.1")
        self.target_port = tk.StringVar(master, value="7001")
        self.allow_broadcast = tk.BooleanVar(master, value=False)

        # UI refs
        self.top_frame: Optional[ttk.Frame] = None
        self.settings_frame: Optional[ttk.Frame] = None

        self.ent_bind_host: Optional[ttk.Entry] = None
        self.ent_bind_port: Optional[ttk.Entry] = None
        self.ent_target_host: Optional[ttk.Entry] = None
        self.ent_target_port: Optional[ttk.Entry] = None
        self.chk_broadcast: Optional[ttk.Checkbutton] = None

        self.lock_widgets: list[tk.Misc] = []

    def build_top(self, parent: ttk.Frame) -> None:
        fr = ttk.Frame(parent)
        self.top_frame = fr

        ttk.Label(fr, text="Bind Host").pack(side="left")
        self.ent_bind_host = ttk.Entry(fr, textvariable=self.bind_host, width=16)
        self.ent_bind_host.pack(side="left", padx=(6, 4))
        ttk.Label(fr, text=":").pack(side="left")
        self.ent_bind_port = ttk.Entry(fr, textvariable=self.bind_port, width=8)
        self.ent_bind_port.pack(side="left", padx=(4, 12))

        ttk.Label(fr, text="Target Host").pack(side="left")
        self.ent_target_host = ttk.Entry(fr, textvariable=self.target_host, width=16)
        self.ent_target_host.pack(side="left", padx=(6, 4))
        ttk.Label(fr, text=":").pack(side="left")
        self.ent_target_port = ttk.Entry(fr, textvariable=self.target_port, width=8)
        self.ent_target_port.pack(side="left", padx=(4, 0))

        self.lock_widgets.extend(
            [w for w in [self.ent_bind_host, self.ent_bind_port, self.ent_target_host, self.ent_target_port] if w is not None]
        )

    def build_settings(self, parent: ttk.Frame) -> None:
        fr = ttk.Frame(parent)
        self.settings_frame = fr

        sec = CollapsibleSection(fr, "UDP Settings", expanded=True)
        sec.pack(fill="x", pady=6)
        box = sec.content

        self.chk_broadcast = ttk.Checkbutton(box, text="Allow Broadcast (SO_BROADCAST)", variable=self.allow_broadcast)
        self.chk_broadcast.pack(anchor="w", padx=6, pady=4)

        ttk.Label(
            box,
            text="UDP is connectionless: bind local endpoint first, then send/receive to target endpoint.",
        ).pack(anchor="w", padx=6, pady=(0, 6))

        if self.chk_broadcast is not None:
            self.lock_widgets.append(self.chk_broadcast)

    def fill_cfg(self, cfg: AppCfg, safe_int: SafeIntFn, safe_float: SafeFloatFn) -> None:
        cfg.udp = UdpCfg(
            bind_host=self.bind_host.get().strip() or "0.0.0.0",
            bind_port=safe_int(self.bind_port.get(), 7001, "UDP bind port", 1, 65535),
            target_host=self.target_host.get().strip() or "127.0.0.1",
            target_port=safe_int(self.target_port.get(), 7001, "UDP target port", 1, 65535),
            allow_broadcast=bool(self.allow_broadcast.get()),
        )

    def can_send(self, stats: Dict[str, Any]) -> bool:
        transport = (stats.get("transport") or "-").lower()
        state = (stats.get("state") or "idle").lower()
        return transport == "udp" and state == "connected"

    def apply_runtime_state(self, stats: Dict[str, Any]) -> None:
        # UDP has no runtime-only controls.
        return

    def apply_tk_colors(self, palette: Dict[str, str]) -> None:
        return
