from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, Message
from StringSessionBot.database.users_mongo import add_user

@Client.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):
    if message.from_user:
        await add_user(message.from_user.id)

    me = await client.get_me()
    mention = me.mention

    await message.reply(
        Data.START.format(message.from_user.mention, mention),
        reply_markup=InlineKeyboardMarkup(Data.buttons)
    )