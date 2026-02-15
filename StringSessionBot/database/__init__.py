from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, MONGO_DB

_client = AsyncIOMotorClient(MONGO_URI)
_db = _client[MONGO_DB]

def get_db():
    return _db