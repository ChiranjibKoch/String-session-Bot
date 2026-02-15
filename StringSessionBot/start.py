import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, Message
from Data import Data
from StringSessionBot.database.users_mongo import add_user

log = logging.getLogger("start")

@Client.on_message(filters.private & filters.command("start"))
async def start_cmd(client: Client, msg: Message):
    if not msg.from_user:
        return

    log.info("START | user=%s", msg.from_user.id)

    try:
        await add_user(msg.from_user.id)
    except Exception:
        log.exception("Failed to add user | user=%s", msg.from_user.id)

    me = await client.get_me()
    mention = me.mention

    await msg.reply(
        Data.START.format(msg.from_user.mention, mention),
        reply_markup=InlineKeyboardMarkup(Data.buttons)
    )