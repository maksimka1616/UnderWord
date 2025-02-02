
from telethon import events
from config import client

def register_handlers():
    handlers = []

    @client.on(events.NewMessage(pattern='^/2$'))
    async def two_command(event):
        await event.edit("2")

    handlers.append(two_command)
    return handlers