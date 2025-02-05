# Mine.py

import re
import time
import asyncio
from telethon import events
from config import client, owner
from other import get_mining_state, set_mining_state, get_mining_kd, set_mining_kd, format_duration

PlazmC = 0
MiningC = 0
KonvertC = 0
RkonvertC = 0
CaseC = 0
RcaseC = 0
MCaseC = 0
DCaseC = 0
KrCaseC = 0
PseC = 0
SspC = 0
EcipC = 0
ZvC = 0
MiningST = None
MiningDS = ""

Boosters = {
    "money": {"⚪️": 0, "🟢": 0, "🔵": 0, "🟣": 0, "🟡": 0, "🟠": 0},
    "ore": {"⚪️": 0, "🟢": 0, "🔵": 0, "🟣": 0, "🟡": 0, "🟠": 0},
    "plasma": {"⚪️": 0, "🟢": 0, "🔵": 0, "🟣": 0, "🟡": 0, "🟠": 0}
}

async def set_mine_kd(event):
    if event.sender_id == owner:
        kd = float(event.pattern_match.group(1))
        set_mining_kd(kd)
        await event.delete()

        if kd.is_integer():
            kd_formatted = int(kd)
        else:
            kd_formatted = kd

        await event.respond(f"⚡️⛏️ КД авто-копания установлено на {kd_formatted} секунд ⛏️⚡️")

async def start_mining(event):
    if event.sender_id == owner:
        set_mining_state(True)
        await event.delete()
        await event.respond("⚡️⛏️ Авто Копание Включено ⛏️⚡️")
        await auto_mine()

async def auto_mine():
    global PlazmC, MiningC, MiningST, MiningDS, KonvertC, RkonvertC, CaseC, RcaseC, MCaseC, DCaseC, KrCaseC, PseC, SspC, EcipC, ZvC

    PlazmC = 0
    MiningC = 0
    KonvertC = 0
    RkonvertC = 0
    CaseC = 0
    RcaseC = 0
    MCaseC = 0
    DCaseC = 0
    KrCaseC = 0
    PseC = 0
    SspC = 0
    EcipC = 0
    ZvC = 0
    MiningST = None
    MiningDS = ""

    while get_mining_state():
        kd = get_mining_kd()
        await client.send_message(7066508668, "коп")
        MiningC += 1

        if MiningST is None:
            MiningST = time.time()

        await asyncio.sleep(kd)

    if MiningST is not None:
        mining_duration = time.time() - MiningST
        MiningDS = format_duration(mining_duration)
    else:
        MiningDS = "0с."

async def process_mining_results(event):
    global PlazmC, KonvertC, RkonvertC, CaseC, RcaseC, MCaseC, DCaseC, KrCaseC, PseC, SspC, EcipC, ZvC

    if "Плазма +" in event.raw_text:
        match = re.search(r"Плазма\s*\+(\d+)", event.raw_text)
        if match:
            plasma_amount = int(match.group(1))
            PlazmC += plasma_amount

    if "Найден Конверт" in event.raw_text:
        match = re.search(r"\+(\d+)", event.raw_text)
        if match:
            KonvertC += int(match.group(1))

    if "Найден Редкий Конверт" in event.raw_text:
        match = re.search(r"\+(\d+)", event.raw_text)
        if match:
            RkonvertC += int(match.group(1))

    if "Найден Кейс" in event.raw_text:
        match = re.search(r"\+(\d+)", event.raw_text)
        if match:
            CaseC += int(match.group(1))

    if "Найден Редкий Кейс" in event.raw_text:
        match = re.search(r"\+(\d+)", event.raw_text)
        if match:
            RcaseC += int(match.group(1))

    if "Найден Мифический Кейс" in event.raw_text:
        match = re.search(r"\+(\d+)", event.raw_text)
        if match:
            MCaseC += int(match.group(1))

    if "Найден Дайс Кейс" in event.raw_text:
        match = re.search(r"\+(\d+)", event.raw_text)
        if match:
            DCaseC += int(match.group(1))

    if "Найден Кристальный Кейс" in event.raw_text:
        match = re.search(r"\+(\d+)", event.raw_text)
        if match:
            KrCaseC += int(match.group(1))

    if "Найден Портфель c Эскизами" in event.raw_text:
        match = re.search(r"\+(\d+)", event.raw_text)
        if match:
            PseC += int(match.group(1))

    if "Найден Сумка c Предметами" in event.raw_text:
        match = re.search(r"\+(\d+)", event.raw_text)
        if match:
            SspC += int(match.group(1))

    if "Найден Ящик c Экипировкой" in event.raw_text:
        match = re.search(r"\+(\d+)", event.raw_text)
        if match:
            EcipC += int(match.group(1))

    if "💫" in event.raw_text:
        ZvC += 1

    if "Найден бустер" in event.raw_text:
        match = re.search(r"⚡️(💰|⛏️|🔮)(⚪️|🟢|🔵|🟣|🟡|🟠)\s*([^\(]+)\s*\(\d+ мин.\)", event.raw_text)
        if match:
            booster_type = match.group(1)
            booster_level = match.group(2)
            booster_name = match.group(3).strip()

            if booster_type == "💰":
                Boosters["money"][booster_level] += 1
            elif booster_type == "⛏️":
                Boosters["ore"][booster_level] += 1
            elif booster_type == "🔮":
                Boosters["plasma"][booster_level] += 1

async def stop_mining(event):
    global MiningST, MiningDS, MiningC, PlazmC, KonvertC, RkonvertC, CaseC, RcaseC, MCaseC, DCaseC, KrCaseC, PseC, SspC, EcipC, ZvC

    if event.sender_id == owner:
        set_mining_state(False)
        await event.delete()

        if MiningST is not None:
            mining_duration = time.time() - MiningST
            MiningDS = format_duration(mining_duration)
        else:
            MiningDS = "0с."

        boosters_message = (
            f"💰:\n"
            f"⚪️: {Boosters['money']['⚪️']}|🟢: {Boosters['money']['🟢']}|🔵: {Boosters['money']['🔵']}\n"
            f"🟣: {Boosters['money']['🟣']}|🟡: {Boosters['money']['🟡']}|🟠: {Boosters['money']['🟠']}\n"
            f"⛏️:\n"
            f"⚪️: {Boosters['ore']['⚪️']}|🟢: {Boosters['ore']['🟢']}|🔵: {Boosters['ore']['🔵']}\n"
            f"🟣: {Boosters['ore']['🟣']}|🟡: {Boosters['ore']['🟡']}|🟠: {Boosters['ore']['🟠']}\n"
            f"🔮:\n"
            f"⚪️: {Boosters['plasma']['⚪️']}|🟢: {Boosters['plasma']['🟢']}|🔵: {Boosters['plasma']['🔵']}\n"
            f"🟣: {Boosters['plasma']['🟣']}|🟡: {Boosters['plasma']['🟡']}|🟠: {Boosters['plasma']['🟠']}\n"
        )

        await event.respond(f"⚡️⛏️ Копание Выключено⛏️⚡️\n\n"
                            f"⌛️ UnderWord UserBot копал {MiningDS}\n"
                            f"📨 Всего копаний сделано: {MiningC}\n\n"
                            f"⬇️ За этот период ты выкопал ⬇️\n\n"
                            f"🎆 Плазмы: {PlazmC}\n"
                            f"✉️ Конвертов: {KonvertC}\n"
                            f"🧧 Редких Конвертов: {RkonvertC}\n"
                            f"📦 Кейсов: {CaseC}\n"
                            f"🗳 Редких Кейсов: {RcaseC}\n"
                            f"🕋 Мифических Кейсов: {MCaseC}\n"
                            f"🎲 Дайс Кейсов: {DCaseC}\n"
                            f"💎 Кристальных Кейсов: {KrCaseC}\n"
                            f"💼 Портфелей с Эскизами: {PseC}\n"
                            f"👜 Сумок с Предметами: {SspC}\n"
                            f"🧰 Ящиков с Экипировкой: {EcipC}\n"
                            f"🌌 зв: {ZvC}\n\n"
                            f"Бустеры:\n\n"
                            f"{boosters_message}")

def register_handlers():
    @client.on(events.NewMessage(pattern='^/minekd (\d+(\.\d+)?)$'))
    async def set_mine_kd_handler(event):
        await set_mine_kd(event)

    @client.on(events.NewMessage(pattern='^/minestart$'))
    async def start_mining_handler(event):
        await start_mining(event)

    @client.on(events.NewMessage(chats=7066508668))
    async def process_mining_results_handler(event):
        await process_mining_results(event)

    @client.on(events.NewMessage(pattern='^/minestop$'))
    async def stop_mining_handler(event):
        await stop_mining(event)