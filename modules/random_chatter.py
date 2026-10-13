import random

from textual.containers import VerticalScroll

from .chat import ChatMessage

USERS = [
    ("Jake", "Apollo"),
    ("Mia", "Zeus"),
    ("Sam", "Hera"),
    ("Luna", "Athena"),
    ("Max", "Ares"),
    ("Zoe", "Artemis"),
    ("Leo", "Hermes"),
    ("Nina", "Demeter"),
    ("Finn", "Poseidon"),
    ("Ruby", "Hestia"),
    ("Kai", "Dionysus"),
    ("Ella", "Persephone"),
]

LINES = [
    "hey",
    "what's up?",
    "anyone here?",
    "lol",
    "good morning!",
    "brb",
    "did you see that?",
    "no way",
    "haha same",
    "that's wild",
    "ok cool",
    "wait, what happened?",
    "I'm back",
    "who's up for a game later?",
    "thanks!",
    "sounds good to me",
    "interesting...",
    "can someone help me out?",
    "just got here",
    "gg",
]

def send_random_message(chat_log: VerticalScroll) -> None:
    at_bottom = chat_log.scroll_y >= chat_log.max_scroll_y - 1

    user, uid = random.choice(USERS)
    chat_log.mount(ChatMessage(user, random.choice(LINES), uid))

    if at_bottom:
        chat_log.scroll_end(animate=True)
