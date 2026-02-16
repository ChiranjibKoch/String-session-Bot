import logging
import asyncio
import speedtest
from pyrogram import Client, filters
from pyrogram.types import Message
from StringSessionBot.database.users_mongo import num_users

log = logging.getLogger("admin")

ADMIN_ID = 5218610039

def testspeed():
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    return test.results.dict()

@Client.on_message(filters.user(ADMIN_ID) & filters.command("stats"))
async def stats_cmd(client: Client, msg: Message):
    log.info("STATS | user=%s", msg.from_user.id if msg.from_user else None)
    try:
        users = await num_users()
        await msg.reply(f"Total Users : {users}")
    except Exception:
        log.exception("Stats failed")
        await msg.reply("Failed to fetch stats.")

@Client.on_message(filters.user(ADMIN_ID) & filters.command("speedtest"))
async def speedtest_cmd(client: Client, msg: Message):
    log.info("SPEEDTEST | user=%s", msg.from_user.id if msg.from_user else None)

    m = await msg.reply("Running speed test…")

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, testspeed)

        output = f"""**Speedtest Results**

**Client:**
ISP: {result['client']['isp']}
Country: {result['client']['country']}

**Server:**
Name: {result['server']['name']}
Country: {result['server']['country']}, {result['server']['cc']}
Sponsor: {result['server']['sponsor']}
Latency: {result['server']['latency']}
Ping: {result['ping']}
"""

        await client.send_photo(
            chat_id=msg.chat.id,
            photo=result["share"],
            caption=output
        )
        await m.delete()

    except Exception:
        log.exception("Speedtest failed")
        await m.edit("Speedtest failed.")

@Client.on_message(filters.user(ADMIN_ID) & filters.command("broadcast"))
async def broadcast_cmd(client: Client, msg: Message):
    log.info("BROADCAST | user=%s", msg.from_user.id if msg.from_user else None)

    if msg.reply_to_message:
        content = msg.reply_to_message
    else:
        if len(msg.command) < 2:
            await msg.reply("Use: `/broadcast your message` or reply to a message with `/broadcast`")
            return
        content = msg.text.split(None, 1)[1]

    users = await get_all_users()

    sent = 0
    failed = 0

    status = await msg.reply("Broadcast started…")

    for u in users:
        user_id = u["_id"]
        try:
            if isinstance(content, Message):
                await content.copy(chat_id=user_id)
            else:
                await client.send_message(chat_id=user_id, text=content)
            sent += 1
            await asyncio.sleep(0.1)
        except Exception:
            failed += 1

    await status.edit(f"Broadcast finished.\n\nSent: {sent}\nFailed: {failed}")