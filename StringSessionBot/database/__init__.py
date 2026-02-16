import logging
from motor.motor_asyncio import AsyncIOMotorClient
import config

log = logging.getLogger("database")

_client = None
_db = None

def get_db():
    global _client, _db

    if _db is not None:
        return _db

    try:
        _client = AsyncIOMotorClient(
            config.MONGO_URI,
            serverSelectionTimeoutMS=5000
        )
        _db = _client[config.MONGO_DB]
        return _db
    except Exception:
        log.exception("Failed to connect to MongoDB")
        return None