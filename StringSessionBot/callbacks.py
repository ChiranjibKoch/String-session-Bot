from Data import Data
from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, LinkPreviewOptions
from StringSessionBot.generate import generate_session, ERROR_MESSAGE

@Client.on_callback_query()
async def callbacks(client: Client, cq: CallbackQuery):
    me = await client.get_me()
    mention = me.mention
    query = (cq.data or "").lower()

    try:
        if query == "home":
            await cq.message.edit_text(
                Data.START.format(cq.from_user.mention, mention),
                reply_markup=InlineKeyboardMarkup(Data.buttons),
            )

        elif query == "about":
            await cq.message.edit_text(
                Data.ABOUT,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
                reply_markup=InlineKeyboardMarkup(Data.home_buttons),
            )

        elif query == "help":
            await cq.message.edit_text(
                "**Here's How to use me**\n" + Data.HELP,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
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

        elif query == "gen_pyrogram":
            await cq.answer()
            await generate_session(
                client,
                chat_id=cq.message.chat.id,
                user_id=cq.from_user.id,
                telethon=False
            )

        elif query == "gen_telethon":
            await cq.answer()
            await generate_session(
                client,
                chat_id=cq.message.chat.id,
                user_id=cq.from_user.id,
                telethon=True
            )

        else:
            await cq.answer("Unknown action", show_alert=False)

    except Exception as e:
        await cq.message.reply(ERROR_MESSAGE.format(str(e)))