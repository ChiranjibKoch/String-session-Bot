from pyrogram import Client, filters
from pyrogram.types import Message
from StringSessionBot.database.users_mongo import add_user, num_users

ADMIN_ID = 5218610039

@Client.on_message(filters.private, group=1)
async def track_users(client: Client, message: Message):
    if message.from_user:
        await add_user(message.from_user.id)

@Client.on_message(filters.user(ADMIN_ID) & filters.command("stats"))
async def stats_cmd(client: Client, message: Message):
    users = await num_users()
    await message.reply(f"Total Users : {users}")