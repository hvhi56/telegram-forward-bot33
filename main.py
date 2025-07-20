from telethon import TelegramClient, events
import os
import re

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")
channel = os.getenv("CHANNEL")
bot_username = os.getenv("BOT_USERNAME")

ALLOWED_LINKS = [
    "t.me/hamoked_il",
    "chat.whatsapp.com/LoxVwdYOKOAH2y2kaO8GQ7",
    "t.me/Moshepargod"
]

link_pattern = re.compile(r'(https?://\S+|t\.me/\S+)', re.IGNORECASE)

def should_forward(message):
    content = message.text or ""

    links = link_pattern.findall(content)
    if not links:
        return True

    for link in links:
        for allowed in ALLOWED_LINKS:
            if allowed in link:
                return True
    return False

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(chats=channel))
async def handler(event):
    if should_forward(event.message):
        await event.message.forward_to(bot_username)
    else:
        print("❌ נחסמה הודעה עם קישור לא מורשה")

async def main():
    print("מתחבר...")
    await client.start(phone=phone)
    print(f"רץ ומעביר הודעות מ‑{channel} → {bot_username} (ללא קישורים לא מורשים)")
    await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
