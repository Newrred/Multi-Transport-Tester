from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Protocol

import tkinter as tk
from tkinter import ttk


SafeIntFn = Callable[[str, int, str, Optional[int], Optional[int]], int]
SafeFloatFn = Callable[[str, float, str, Optional[float], Optional[float]], float]


class TransportUI(Protocol):
    """Transport UI plugin contract.

    App은 이 인터페이스만 알고 transport 별 UI/CFG 로직은 플러그인이 소유합니다.
    """

    name: str

    # UI containers (App이 show/hide)
    top_frame: ttk.Frame
    settings_frame: ttk.Frame

    # widgets to lock when running
    lock_widgets: List[tk.Misc]

    def build_top(self, parent: ttk.Frame) -> None: ...

    def build_settings(self, parent: ttk.Frame) -> None: ...

    def fill_cfg(self, cfg: Any, safe_int: SafeIntFn, safe_float: SafeFloatFn) -> None: ...

    def can_send(self, stats: Dict[str, Any]) -> bool: ...

    def apply_runtime_state(self, stats: Dict[str, Any]) -> None: ...

    def apply_tk_colors(self, palette: Dict[str, str]) -> None: ...


@dataclass
class TransportCallbacks:
    """플러그인이 App/Engine으로 신호를 보내야 할 때 사용하는 콜백 묶음."""

    # tcp server target(scope/selection) 변경을 엔진에 반영
    on_tcp_targets_changed: Optional[Callable[[bool], None]] = None
