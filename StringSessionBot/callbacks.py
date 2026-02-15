from Data import Data
from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from StringSessionBot.generate import ERROR_MESSAGE

@Client.on_callback_query()
async def callbacks(bot: Client, cq: CallbackQuery):
    user = await bot.get_me()
    mention = user["mention"]
    query = (cq.data or "").lower()

    chat_id = cq.from_user.id
    message_id = cq.message.message_id

    try:
        if query == "home":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=Data.START.format(cq.from_user.mention, mention),
                reply_markup=InlineKeyboardMarkup(Data.buttons),
            )

        elif query == "about":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=Data.ABOUT,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(Data.home_buttons),
            )

        elif query == "help":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="**Here's How to use me**\n" + Data.HELP,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(Data.home_buttons),
            )

        elif query == "generate":
            await cq.message.reply(
                "Please choose which string session you want to generate:",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Pyrogram", callback_data="gen_pyrogram"),
                    InlineKeyboardButton("Telethon", callback_data="gen_telethon")
                ]])
            )

        elif query in ["gen_pyrogram", "gen_telethon"]:
            await cq.answer()
            if query == "gen_pyrogram":
                await cq.message.reply("Starting Pyrogram session generation…\nPlease send your `API_ID`")
            else:
                await cq.message.reply("Starting Telethon session generation…\nPlease send your `API_ID`")

        else:
            await cq.answer("Unknown action", show_alert=False)

    except Exception as e:
        await cq.message.reply(ERROR_MESSAGE.format(str(e)))