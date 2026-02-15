from pyrogram.types import InlineKeyboardButton


class Data:
    START = """
Hello {}

If you don't trust this bot:
1) Don't use it
2) Block the bot or delete the chat

This bot helps you generate Pyrogram and Telethon string sessions.
For safety, always use a secondary account.

Managed by @ArchAssociation
    """

    home_buttons = [
        [InlineKeyboardButton("Start Generating Session", callback_data="generate")],
        [InlineKeyboardButton(text="Home", callback_data="home")]
    ]

    generate_button = [
        [InlineKeyboardButton("Start Generating Session", callback_data="generate")]
    ]

    buttons = [
        [InlineKeyboardButton("Start Generating Session", callback_data="generate")],
        [InlineKeyboardButton("Maintained By", url="https://t.me/ArchAssociation")],
        [
            InlineKeyboardButton("How to use me", callback_data="help"),
            InlineKeyboardButton("About", callback_data="about")
        ],
        [InlineKeyboardButton("Support", url="https://t.me/ArchAssociation")]
    ]

    HELP = """
✨ **Available Commands** ✨

/about - About this bot
/help - How to use this bot
/start - Start the bot
/generate - Start generating a session
/cancel - Cancel the current process
/restart - Restart the bot
"""

    ABOUT = """
🌟 **About This Bot** 🌟

This is a Telegram bot to generate **Pyrogram** and **Telethon** string sessions.

🔧 **Framework:** https://docs.kurigram.icu/  
🐍 **Language:** https://www.python.org/  
🛠 **Purpose:** Generate safe session strings for Telegram clients  

📢 **Support & Updates:** https://t.me/ArchAssociation  
👤 **Maintained by:** @ArchAssociation
    """