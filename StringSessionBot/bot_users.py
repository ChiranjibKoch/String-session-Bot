from pyrogram import Client, filters
from pyrogram.types import Message
from StringSessionBot.database.users_mongo import add_user, num_users

@Client.on_message(~filters.service, group=1)
async def track_users(_, msg: Message):
    if msg.from_user:
        await add_user(msg.from_user.id)

@Client.on_message(filters.user(5218610039) & filters.command("stats"))
async def stats_cmd(_, msg: Message):
    users = await num_users()
    await msg.reply(f"Total Users : {users}", quote=True)