from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
import config

@Client.on_message(filters.private, group=-1)
async def must_join_channel(client: Client, message: Message):
    if not config.MUST_JOIN or not message.from_user:
        return

    try:
        try:
            await client.get_chat_member(config.MUST_JOIN, message.from_user.id)
        except UserNotParticipant:
            if config.MUST_JOIN.isalpha():
                link = "https://t.me/" + config.MUST_JOIN
            else:
                chat_info = await client.get_chat(config.MUST_JOIN)
                link = chat_info.invite_link

            try:
                await message.reply(
                    f"You must join [this channel]({link}) to use me. After joining try again!",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("✨ Join Channel ✨", url=link)]
                    ])
                )
                await message.stop_propagation()
            except ChatWriteForbidden:
                pass

    except ChatAdminRequired:
        print(f\"I'm not admin in the MUST_JOIN chat: {config.MUST_JOIN}!\")