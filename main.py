from typing import ClassVar

import socketio
from socketio.exceptions import ConnectionError
from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.widgets import Footer, Header

from modules.chat import ChatRoom, send_msg

# from modules.random_chatter import send_random_message

USERNAME = "Apollo"
SERVER_URL = "http://127.0.0.1:5000/"
sock = socketio.AsyncClient()


class Application(App):
    AUTO_FOCUS = "#message_input"
    BINDINGS: ClassVar[list[BindingType]] = [("d", "toggle_dark", "Toggle dark modes")]

    CSS = """
        #chat_log {
            height: 1fr;
        }

        #message_holder {
            height: auto;
            # dock: bottom;
        }

        #message_input {
            width: 1fr;
        }

        #message_holder Button {
            width: auto;
            min-width: 10;
        }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield ChatRoom(sock, USERNAME, id="message_holder")
        yield Footer()

    def on_mount(self) -> None:
        self.run_worker(self.connect())

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    async def connect(self) -> None:
        async def on_message(data):
            send_msg(self, data["user"], data["data"] )

        try:
            await sock.connect(SERVER_URL, transports=["websocket"], auth={"user": USERNAME})
        except ConnectionError as e:
            self.notify(f"{e!r}", severity="error")

        sock.on("server_message", on_message)




if __name__ == "__main__":
    Application().run()
