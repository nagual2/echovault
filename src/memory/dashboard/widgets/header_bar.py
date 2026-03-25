"""Custom header bar showing mode, project, and memory count."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static


class HeaderBar(Widget):
    """Top bar: app name | mode | project | count."""

    DEFAULT_CSS = """
    HeaderBar {
        dock: top;
        height: 1;
        layout: horizontal;
        background: $accent;
        color: $text;
    }

    HeaderBar .hdr-left {
        width: auto;
        padding: 0 1;
        text-style: bold;
    }

    HeaderBar .hdr-spacer {
        width: 1fr;
    }

    HeaderBar .hdr-right {
        width: auto;
        padding: 0 1;
    }
    """

    mode: reactive[str] = reactive("overview")
    project: reactive[str] = reactive("")
    memory_count: reactive[int] = reactive(0)

    def compose(self) -> ComposeResult:
        yield Static("EchoVault", classes="hdr-left")
        yield Static(":overview", id="hdr-mode", classes="hdr-left")
        yield Static("", classes="hdr-spacer")
        yield Static("all projects", id="hdr-project", classes="hdr-right")
        yield Static("0 memories", id="hdr-count", classes="hdr-right")

    def watch_mode(self, value: str) -> None:
        try:
            self.query_one("#hdr-mode", Static).update(f":{value}")
        except Exception:
            pass

    def watch_project(self, value: str) -> None:
        try:
            self.query_one("#hdr-project", Static).update(value or "all projects")
        except Exception:
            pass

    def watch_memory_count(self, value: int) -> None:
        try:
            self.query_one("#hdr-count", Static).update(f"{value} memories")
        except Exception:
            pass
