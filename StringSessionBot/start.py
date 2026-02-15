from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from StringSessionBot.database.users_mongo import add_user

@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def start(bot, msg):
    await add_user(msg.from_user.id)
    me = await bot.get_me()
    mention = me["mention"]
    await bot.send_message(
        msg.chat.id,
        Data.START.format(msg.from_user.mention, mention),
        reply_markup=InlineKeyboardMarkup(Data.buttons)
    )