# Apollinaris

A terminal chat app (TUI) built with [Textual](https://textual.textualize.io/) that talks to a server over WebSockets using [Socket.IO](https://python-socketio.readthedocs.io/).

> [!WARNING]
> **This is a side project.** It was built for fun and learning, and it is **not** intended for serious work. Do not use it for anything important, anything sensitive, or anything that needs to be reliable or secure.

> [!NOTE]
> The project is in a very early state (version `0.1.0`). Expect missing features, rough edges, and breaking changes.

## Table of contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [How it works](#how-it-works)
- [Known problems](#known-problems)
- [License](#license)

## Features

- Full-screen chat interface in your terminal
- Real-time messaging over WebSockets
- Light and dark themes (press `d` to toggle)
- Connection errors are shown as in-app notifications

## Requirements

- Python **3.13** or newer
- [uv](https://docs.astral.sh/uv/) (the repo ships a `uv.lock` and `.python-version`)
- A running Socket.IO chat server that speaks the protocol described in [How it works](#how-it-works)

> [!IMPORTANT]
> Apollinaris is only the **client**. Without a compatible server running, the app will start but you will not be able to chat.

## Installation

```bash
git clone https://github.com/E1480/Apollinaris.git
cd Apollinaris
uv sync
```

> [!NOTE]
> The client's dependencies (`textual`, `rich`, `python-socketio` and `aiohttp`) are regular project dependencies. `uv sync` also installs the `dev` group by default, which contains `flask` and `flask-socketio` for running a test server.

## Usage

Start your server first, then run the client:

```bash
uv run main.py
```

| Key | Action                 |
| --- | ---------------------- |
| `d` | Toggle light/dark mode |

> [!TIP]
> The message input is focused automatically on launch, so you can start typing straight away.

## Configuration

There is no config file or command-line options yet. Settings are constants at the top of `main.py`:

```python
USERNAME = "Apollo"
SERVER_URL = "http://127.0.0.1:5000/"
```

> [!CAUTION]
> Edit `main.py` directly to change your username or server address. Anyone using the same `USERNAME` will be indistinguishable from you.

## How it works

On startup the client connects to `SERVER_URL` using the `websocket` transport and sends the username as connection auth data:

```python
auth={"user": USERNAME}
```

Incoming messages are received through the `server_message` event, and each payload is expected to look like this:

```json
{ "user": "<sender name>", "data": "<message text>" }
```

The UI is built from Textual widgets (header, chat room, footer), and the chat widgets live in the `modules/` package.

## Known problems

> [!WARNING]
> This list is not exhaustive. It covers the issues I know about.

**Setup and packaging**

- **No server setup documented.** `flask` and `flask-socketio` are dev-only dependencies, and the project does not yet describe how to run a compatible server.
- **Placeholder metadata.** The package is named `tui` with an empty description.
- **Python 3.13+ only.** Older Python versions are not supported.

**Configuration**

- **Hardcoded username and server URL.** Changing them means editing the source.
- **No UI for choosing a username or server** at startup.

**Connection handling**

- **No reconnection logic.** If the server is down at launch, you get an error notification and the app stays offline until you restart it.
- **Late event handler registration.** The `server_message` handler is registered *after* the connection attempt, so messages sent immediately on connect could be missed.
- **Limited error handling.** Only the initial connection error is handled, and other failures (dropped connections, malformed payloads) are not.

**Security**

> [!CAUTION]
> There is **no real authentication**. The "auth" is just a username string that anyone can claim, and the default URL uses plain `http://`, so traffic is **not encrypted**. Do not send anything private.

**UI**

- **Theme toggle quirk.** The `d` key only switches between `textual-dark` and `textual-light`. If another Textual theme is active, pressing it will switch to light mode.
- **No message history.** Messages exist only for the current session.
- **No user list, rooms, or private messages.**

**Testing and maintenance**

- A `tests/` folder exists, but test coverage and CI are minimal or absent.
- A `random_chatter` helper is imported in `main.py` but commented out, so it looks like leftover debugging code.

## License

Released under the [MIT License](LICENSE).

> [!NOTE]
> The software is provided "as is", without warranty of any kind. See the license for details.
