from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, Message

@Client.on_message(filters.private & filters.command("about"))
async def about_cmd(client: Client, message: Message):
    await message.reply(
        Data.ABOUT,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons),
    )