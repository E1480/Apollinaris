import hashlib
import os

import socketio
from rich.text import Text
from textual import on
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Input, Rule, Static

COLORS = ["green", "red", "yellow", "cyan", "magenta", "blue", "orange1", "deep_pink2"]

def get_user_color(uid: str) -> str:
    digest = hashlib.sha256(uid.encode()).digest()
    index = int.from_bytes(digest[:4], "big") % len(COLORS)
    return COLORS[index]

def send_msg(app, user_name: str, message: str, seed: str = f"{os.urandom(16)}"):
    chat_log = app.query_one("#chat_log", VerticalScroll)

    chat_log.mount(
        ChatMessage(
            user_name,
            message,
            hashlib.md5(user_name.replace("(You)", seed).encode()).hexdigest(),
        )
    )

    chat_log.scroll_end(animate=False)

class ChatMessage(Static):
    def __init__(self, user_name: str, message: str, uid: str, local_color: str = "white"):
        super().__init__()
        self.user_name = user_name
        self.message = message
        self.uid = uid
        self.local_color = local_color


    def render(self) -> Text:
        text = Text()
        text.append(self.user_name, style=f"bold {self.local_color}")
        text.append(f": {self.message}")
        return text

    #TODO: Make functional
    def on_click(self) -> None:
        if self.user_name == "You" or self.uid == "me":
            return
        self.app.notify(f"Sent P2P To {self.user_name}#{hashlib.sha256(self.uid.encode()).hexdigest()[:5]}")

class ChatRoom(Vertical):


    def __init__(self, sock: socketio.AsyncClient, user_name: str, **kwargs):
        super().__init__(**kwargs)
        self.sock = sock
        self.user_name = user_name

    def compose(self):

        yield VerticalScroll(id="chat_log")
        yield Rule(line_style="double", id="separator")
        with Horizontal(id="message_holder"):
            yield Input(
                placeholder="Enter a message...", type="text", id="message_input"
            )
            yield Button(label="Send", id="send_message")

        yield Rule(line_style="none")

    async def on_unmount(self) -> None:
        if self.sock.connected:
            await self.sock.disconnect()

    @on(Button.Pressed, "#send_message")
    @on(Input.Submitted, "#message_input")
    async def send_message(self) -> None:
        input_widget = self.query_one("#message_input", Input)
        text = input_widget.value.strip()
        if not text:
            return
        send_msg(self, f"{self.user_name}(You)", text)
        if self.sock.connected:
            await self.sock.emit("chat_message", {"user": self.user_name, "message": text})
        input_widget.value = ""
        input_widget.focus()
