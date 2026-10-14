from typing import cast

from flask import Flask, Request, render_template_string, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
users: dict[str, str] = {}

SERVER_NAME = "[SERVER]"


class SocketRequest(Request):
    sid: str


def get_sid():
    return cast(SocketRequest, request).sid


@app.route("/")
def index():
    return render_template_string(HTML)


@socketio.on("connect")
def on_connect(auth):
    user = (auth or {}).get("user", "Anonymous")
    users[get_sid()] = user
    print(f"Client connected {users}")
    emit(
        "server_message",
        {"user": SERVER_NAME, "data": f"{users.get(get_sid())} has connected."},
        broadcast=True,
    )


@socketio.on("chat_message")
def on_chat_message(data):
    print("Received:", data)
    # Broadcast to every connected client
    emit(
        "server_message",
        {"user": users.get(get_sid(), "Anonymous"), "data": data["message"]},
        broadcast=True,
        include_self=False,
    )


@socketio.on("disconnect")
def on_disconnect():
    print(f"Client disconnected {users[get_sid()]}")
    emit(
        "server_message",
        {"user": "[SERVER]", "data": f"{users.pop(get_sid(), 'Anonymous')} has left."},
        broadcast=True,
    )


HTML = """
    <!DOCTYPE html>
    <html>
    <body>
      <input id="msg" placeholder="Type a message">
      <button onclick="send()">Send</button>
      <ul id="log"></ul>

      <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
      <script>
        const socket = io();  // connects to the same host

        # socket.on("server_message", (msg) => {
        #   const li = document.createElement("li");
        #   li.textContent = msg.data;
        #   document.getElementById("log").appendChild(li);
        # });

        socket.on("client")

        function send() {
          const input = document.getElementById("msg");
          socket.emit("chat_message", {user: SERVER_NAME, message: input.value });
          input.value = "";
        }
      </script>
    </body>
    </html>
"""

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
