import asyncio
import speedtest
from pyrogram import Client, filters
from pyrogram.types import Message
from StringSessionBot.database import get_db

ADMIN_ID = 5218610039

def testspeed():
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    return test.results.dict()

@Client.on_message(filters.user(ADMIN_ID) & filters.command("speedtest"))
async def speedtest_cmd(client: Client, message: Message):
    m = await message.reply_text("Running Speed test…")
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(None, testspeed)
    except Exception as e:
        await m.edit(f"Speedtest failed: {e}")
        return

    output = f"""**Speedtest Results**

<u>**Client:**</u>
**__ISP:__** {result['client']['isp']}
**__Country:__** {result['client']['country']}

<u>**Server:**</u>
**__Name:__** {result['server']['name']}
**__Country:__** {result['server']['country']}, {result['server']['cc']}
**__Sponsor:__** {result['server']['sponsor']}
**__Latency:__** {result['server']['latency']}
**__Ping:__** {result['ping']}
"""

    await client.send_photo(chat_id=message.chat.id, photo=result["share"], caption=output)
    await m.delete()

@Client.on_message(filters.user(ADMIN_ID) & filters.command("broadcast"))
async def broadcast_cmd(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply("Reply to a message with /broadcast")
        return

    status = await message.reply("Broadcast started…")
    db = get_db()
    users = db.users

    sent = 0
    failed = 0

    async for user in users.find({}, {"_id": 1}):
        try:
            await message.reply_to_message.copy(chat_id=user["_id"])
            sent += 1
        except Exception:
            failed += 1

    await status.edit(f"Broadcast finished.\n\nSent: {sent}\nFailed: {failed}")