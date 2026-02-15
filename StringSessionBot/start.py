from pyrogram import Client, filters

@Client.on_message(filters.private)
async def probe(bot, msg):
    await msg.reply("✅ I received your message")