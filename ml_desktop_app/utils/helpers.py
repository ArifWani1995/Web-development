from __future__ import annotations

import tkinter as tk
from tkinter import ttk

PALETTE = {
    "bg": "#0f172a",
    "sidebar": "#111827",
    "surface": "#1f2937",
    "card": "#334155",
    "primary": "#22d3ee",
    "accent": "#a78bfa",
    "text": "#e2e8f0",
    "muted": "#94a3b8",
}

LIGHT_PALETTE = {
    "bg": "#f1f5f9",
    "sidebar": "#e2e8f0",
    "surface": "#ffffff",
    "card": "#cbd5e1",
    "primary": "#0ea5e9",
    "accent": "#7c3aed",
    "text": "#0f172a",
    "muted": "#475569",
}


class ToolTip:
    def __init__(self, widget: tk.Widget, text: str) -> None:
        self.widget = widget
        self.text = text
        self.tip_window: tk.Toplevel | None = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, _: tk.Event) -> None:
        if self.tip_window:
            return
        x, y, _, _ = self.widget.bbox("insert") if self.widget.winfo_exists() else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 16
        y += self.widget.winfo_rooty() + 24
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")
        label = ttk.Label(self.tip_window, text=self.text, padding=6)
        label.pack()

    def hide_tip(self, _: tk.Event) -> None:
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


def apply_theme(root: tk.Tk, dark_mode: bool) -> dict[str, str]:
    colors = PALETTE if dark_mode else LIGHT_PALETTE
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("App.TFrame", background=colors["bg"])
    style.configure("Surface.TFrame", background=colors["surface"])
    style.configure("Card.TFrame", background=colors["card"])
    style.configure("Title.TLabel", background=colors["surface"], foreground=colors["text"], font=("Segoe UI", 18, "bold"))
    style.configure("Body.TLabel", background=colors["surface"], foreground=colors["text"], font=("Segoe UI", 10))
    style.configure("Sidebar.TButton", background=colors["sidebar"], foreground=colors["text"], font=("Segoe UI", 10, "bold"), padding=8)
    style.map("Sidebar.TButton", background=[("active", colors["primary"])], foreground=[("active", colors["bg"])])
    style.configure("Accent.TButton", background=colors["primary"], foreground=colors["bg"], font=("Segoe UI", 10, "bold"), padding=8)
    style.map("Accent.TButton", background=[("active", colors["accent"])])
    style.configure("TLabel", background=colors["surface"], foreground=colors["text"])
    style.configure("TEntry", fieldbackground=colors["bg"], foreground=colors["text"])
    style.configure("TCombobox", fieldbackground=colors["bg"], foreground=colors["text"])
    return colors
