from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, Message, LinkPreviewOptions

@Client.on_message(filters.private & filters.command("about"))
async def about_cmd(bot: Client, msg: Message):
    await bot.send_message(
        msg.chat.id,
        Data.ABOUT,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        reply_markup=InlineKeyboardMarkup(Data.home_buttons),
    )