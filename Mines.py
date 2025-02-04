from telethon import events
from config import client, owner
import asyncio

chat_ids = ['@mine_evo_bot', '@mine_evo_emerald_bot', '@mine_evo_gold_bot', '@mine_evo_ruby_bot']
delay_times = [2, 1.5, 1.5, 1.5]

sending_enabled = False
task = None

async def send_messages():
    global sending_enabled
    while True:
        if sending_enabled:
            for chat_id, delay in zip(chat_ids, delay_times):
                await client.send_message(chat_id, "коп")
                await asyncio.sleep(delay)
        else:
            await asyncio.sleep(1)

def register_handlers():
    handlers = []

    @client.on(events.NewMessage(pattern='/startmine'))
    async def start(event):
        if event.sender_id == owner:
            global task
            if task is None:
                task = asyncio.create_task(send_messages())
            await event.edit('Бот запущен. Используйте /mine для включения/выключения отправки сообщений')
        else:
            return

    @client.on(events.NewMessage(pattern='/mine'))
    async def toggle(event):
        if event.sender_id == owner:
            global sending_enabled
            sending_enabled = not sending_enabled
            status = 'включена' if sending_enabled else 'выключена'
            await event.edit(f'Копка {status}.')
        else:
            return

    return handlers
