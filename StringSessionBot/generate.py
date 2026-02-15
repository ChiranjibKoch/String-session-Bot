from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

ERROR_MESSAGE = (
    "Oops! An exception occurred!\n\n**Error** : {}\n\n"
    "Please report this to @ArchAssociation (https://t.me/ArchAssociation). "
    "Sensitive information is not logged by us!"
)

user_states = {}

async def generate_session(client, message, telethon=False):
    user_id = message.from_user.id
    user_states[user_id] = {
        "step": "api_id",
        "telethon": telethon
    }
    await message.reply("Please send your `API_ID`")

@Client.on_message(filters.private & filters.command("generate"))
async def start_generate(client, msg):
    await msg.reply(
        "Please choose which string session you want to generate:",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Pyrogram", callback_data="gen_pyrogram"),
            InlineKeyboardButton("Telethon", callback_data="gen_telethon")
        ]])
    )

@Client.on_message(filters.private)
async def handle_flow(client, msg):
    if not msg.from_user or not msg.text:
        return

    user_id = msg.from_user.id
    text = msg.text.strip()

    if text.lower() in ["/cancel"]:
        if user_id in user_states:
            cleanup(user_id)
            await msg.reply("Generation cancelled.", reply_markup=InlineKeyboardMarkup(Data.generate_button))
        else:
            await msg.reply("No active generation process.")
        return

    if text.lower() in ["/restart", "/generate"]:
        cleanup(user_id)
        await msg.reply(
            "Restarting generation. Please choose:",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Pyrogram", callback_data="gen_pyrogram"),
                InlineKeyboardButton("Telethon", callback_data="gen_telethon")
            ]])
        )
        return

    if user_id not in user_states:
        return

    state = user_states[user_id]

    try:
        if state["step"] == "api_id":
            try:
                state["api_id"] = int(text)
            except ValueError:
                await msg.reply("API_ID must be an integer. Start again.", reply_markup=InlineKeyboardMarkup(Data.generate_button))
                cleanup(user_id)
                return
            state["step"] = "api_hash"
            await msg.reply("Please send your `API_HASH`")

        elif state["step"] == "api_hash":
            state["api_hash"] = text
            state["step"] = "phone"
            await msg.reply("Now send your `PHONE_NUMBER` with country code.\nExample: `+628xxxxxxx`")

        elif state["step"] == "phone":
            state["phone"] = text
            await msg.reply("Sending OTP...")

            if state["telethon"]:
                tg = TelegramClient(StringSession(), state["api_id"], state["api_hash"])
                await tg.connect()
                state["client"] = tg
                await tg.send_code_request(state["phone"])
            else:
                pg = Client(":memory:", state["api_id"], state["api_hash"])
                await pg.connect()
                state["client"] = pg
                sent = await pg.send_code(state["phone"])
                state["code_hash"] = sent.phone_code_hash

            state["step"] = "otp"
            await msg.reply(
                "Check Telegram for the OTP.\n"
                "If OTP is `12345`, send it as: `1 2 3 4 5`"
            )

        elif state["step"] == "otp":
            phone_code = text.replace(" ", "")
            try:
                if state["telethon"]:
                    await state["client"].sign_in(state["phone"], phone_code)
                else:
                    await state["client"].sign_in(state["phone"], state["code_hash"], phone_code)
            except (PhoneCodeInvalid, PhoneCodeInvalidError):
                await msg.reply("OTP is invalid. Start again.", reply_markup=InlineKeyboardMarkup(Data.generate_button))
                cleanup(user_id)
                return
            except (PhoneCodeExpired, PhoneCodeExpiredError):
                await msg.reply("OTP is expired. Start again.", reply_markup=InlineKeyboardMarkup(Data.generate_button))
                cleanup(user_id)
                return
            except (SessionPasswordNeeded, SessionPasswordNeededError):
                state["step"] = "password"
                await msg.reply("Two-step verification is enabled. Please send your password.")
                return

            await finish_session(client, msg, user_id)

        elif state["step"] == "password":
            try:
                if state["telethon"]:
                    await state["client"].sign_in(password=text)
                else:
                    await state["client"].check_password(password=text)
            except (PasswordHashInvalid, PasswordHashInvalidError):
                await msg.reply("Invalid password. Start again.", reply_markup=InlineKeyboardMarkup(Data.generate_button))
                cleanup(user_id)
                return

            await finish_session(client, msg, user_id)

    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply("API_ID and API_HASH combination is invalid.", reply_markup=InlineKeyboardMarkup(Data.generate_button))
        cleanup(user_id)
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply("PHONE_NUMBER is invalid.", reply_markup=InlineKeyboardMarkup(Data.generate_button))
        cleanup(user_id)
    except Exception as e:
        await msg.reply(ERROR_MESSAGE.format(e))
        cleanup(user_id)

async def finish_session(client, msg, user_id):
    state = user_states[user_id]
    if state["telethon"]:
        string_session = state["client"].session.save()
    else:
        string_session = await state["client"].export_session_string()

    text = "**{} STRING SESSION**\n\n`{}`\n\nGenerated by @ArchAssociation".format(
        "TELETHON" if state["telethon"] else "PYROGRAM",
        string_session
    )

    await client.send_message("me", text)
    await state["client"].disconnect()
    await msg.reply("Session generated successfully. Check your Saved Messages.")
    cleanup(user_id)

def cleanup(user_id):
    user_states.pop(user_id, None)