import hashlib
import random
from functools import partial
from typing import ClassVar

from textual import on
from textual.app import App, ComposeResult
from textual.binding import BindingType
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Input

from modules.chat import ChatMessage
from modules.random_chatter import send_random_message

USERNAME = "Apollo"

def send_msg(app, user_name: str, message: str):
    chat_log = app.query_one("#chat_log", VerticalScroll)

    chat_log.mount(
        ChatMessage(
            user_name,
            message,
            hashlib.md5(user_name.encode()).hexdigest()
        )
    )

    chat_log.scroll_end(animate=False)

class Application(App):

    AUTO_FOCUS = "#message_input"
    BINDINGS: ClassVar[list[BindingType]] = [("d","toggle_dark", "Toggle dark modes")]

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

        yield VerticalScroll(id="chat_log")

        # Debug Button
        # yield Button(
        #     label="Add",
        #     id="new_message"
        # )


        with Horizontal(id="message_holder"):

            yield Input(
                placeholder="Enter a message...",
                type="text",
                id="message_input"
            )

            yield Button(
                label="Send",
                id="send_message"
            )

        yield Footer()

    def on_mount(self) -> None:
        chat_log = self.query_one("#chat_log", VerticalScroll)
        self.set_interval(random.random(), partial(send_random_message, chat_log))

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    @on(Button.Pressed, "#send_message")
    @on(Input.Submitted, "#message_input")
    def send_message(self) -> None:
        input_widget = self.query_one("#message_input", Input)
        text = input_widget.value.strip()
        if not text:
            return

        send_msg(self, f"{USERNAME}(You)", text)
        input_widget.value = ""
        input_widget.focus()

    ## Test
    # @on(Button.Pressed, selector="#new_message")
    # def action_new_message(self) -> None:
    #     send_msg(self, "Person", "Welcome!")


if __name__ == '__main__':
    app = Application()
    app.run()
