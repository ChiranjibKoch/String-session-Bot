from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, Message

@Client.on_message(filters.private & filters.incoming & filters.command("help"))
async def help_cmd(bot: Client, msg: Message):
    await bot.send_message(
        msg.chat.id,
        "**Here's how to use me**\n" + Data.HELP,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )