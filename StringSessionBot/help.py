from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, Message

@Client.on_message(filters.private & filters.command("help"))
async def help_cmd(client: Client, message: Message):
    await message.reply(
        "**Here's how to use me**\n" + Data.HELP,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )