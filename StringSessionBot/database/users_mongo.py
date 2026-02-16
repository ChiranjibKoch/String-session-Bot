from StringSessionBot.database import get_db
from . import get_db

async def get_all_users():
    db = get_db()
    cursor = db.users.find({}, {"_id": 1})
    return [doc["_id"] async for doc in cursor]
    
async def add_user(user_id: int):
    db = get_db()
    if not db:
        return
    await db.users.update_one(
        {"_id": user_id},
        {"$setOnInsert": {"_id": user_id}},
        upsert=True
    )

async def num_users() -> int:
    db = get_db()
    if not db:
        return 0
    return await db.users.count_documents({})