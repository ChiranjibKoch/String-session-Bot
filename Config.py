import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.environ.get("ENVIRONMENT", False)

def _get_int(name, default=0):
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        raise Exception(f"{name} is not a valid integer.")

if ENVIRONMENT:
    API_ID = _get_int("API_ID", 0)
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB = os.environ.get("MONGO_DB", "string_session_bot")

    MUST_JOIN = os.environ.get("MUST_JOIN", "")
else:
    API_ID = 0
    API_HASH = ""
    BOT_TOKEN = ""

    MONGO_URI = "mongodb://localhost:27017"
    MONGO_DB = "string_session_bot"

    MUST_JOIN = ""

if MUST_JOIN.startswith("@"):
    MUST_JOIN = MUST_JOIN[1:]