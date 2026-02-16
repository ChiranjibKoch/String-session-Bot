import logging
from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, Message
from StringSessionBot.database.users_mongo import add_user

log = logging.getLogger("plugin.start")

@Client.on_message(filters.private & filters.command("start"))
async def start(bot: Client, msg: Message):
    if not msg.from_user:
        return

    try:
        await add_user(msg.from_user.id)
    except Exception:
        log.exception("Failed to add user to database")
        await msg.reply("⚠️ Database is temporarily unavailable. You can still use the bot, but stats may be inaccurate.")

    try:
        me = await bot.get_me()
        mention = me.mention
    except Exception:
        log.exception("Failed to fetch bot info")
        mention = "this bot"

    await bot.send_message(
        msg.chat.id,
        Data.START.format(msg.from_user.mention, mention),
        reply_markup=InlineKeyboardMarkup(Data.buttons),
    )