import hashlib

from rich.text import Text
from textual.widgets import Static

COLORS = ["green", "red", "yellow", "cyan", "magenta", "blue", "orange1", "deep_pink2"]

def get_user_color(uid: str) -> str:
    digest = hashlib.sha256(uid.encode()).digest()
    index = int.from_bytes(digest[:4], "big") % len(COLORS)
    return COLORS[index]


class ChatMessage(Static):
    def __init__(self, user_name: str, message: str, uid: str):
        super().__init__()
        self.user_name = user_name
        self.message = message
        self.uid = uid


    def render(self) -> Text:
        text = Text()
        text.append(self.user_name, style=f"bold {get_user_color(self.uid)}")
        text.append(f": {self.message}")
        return text

    def on_click(self) -> None:
        if self.user_name == "You" or self.uid == "me":
            return
        self.app.notify(f"Sent P2P To {self.user_name}#{hashlib.sha256(self.uid.encode()).hexdigest()[:5]}")
