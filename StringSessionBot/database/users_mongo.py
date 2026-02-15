from StringSessionBot.database import get_db

db = get_db()
users = db.users

async def add_user(user_id: int):
    await users.update_one(
        {"_id": user_id},
        {"$setOnInsert": {"_id": user_id}},
        upsert=True
    )

async def num_users() -> int:
    return await users.count_documents({})

async def get_all_users():
    return await users.find({}).to_list(length=None)