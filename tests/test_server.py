from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template_string(HTML)

@socketio.on("connect")
def on_connect():
    print("Client connected")
    emit("server_message", {"data": "Welcome!"})

@socketio.on("chat_message")
def on_chat_message(data):
    print("Received:", data)
    # Broadcast to every connected client
    emit("server_message", {"data": data["message"]}, broadcast=True)

@socketio.on("disconnect")
def on_disconnect():
    print("Client disconnected")

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

    socket.on("server_message", (msg) => {
      const li = document.createElement("li");
      li.textContent = msg.data;
      document.getElementById("log").appendChild(li);
    });

    function send() {
      const input = document.getElementById("msg");
      socket.emit("chat_message", { message: input.value });
      input.value = "";
    }
  </script>
</body>
</html>
"""

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
