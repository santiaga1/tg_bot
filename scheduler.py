import asyncio
import logging
import re

from datetime import datetime, time
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

# Get config from .env
from config_reader import config

from db import DB_Connect

# Bot object (bot token from .env)
session = AiohttpSession()
bot = Bot(config.bot_token.get_secret_value(), session=session)
# Dispatcher
dp = Dispatcher(storage=MemoryStorage())

async def send_schedule():
    # Log bot info
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    today_date = datetime.now().strftime('%d.%m')
    #print(today_date)

    db = DB_Connect()
    tasks_list = db.today_tasks(today_date)

    #print(tasks_list)

    for task in tasks_list:
        if(re.search(r"день рожден", task[1].lower())):
            schedule_message = "<b>🎉 Сегодня День Рождения у "+task[2]+"! 🎉\n\n🎁 Поздравляем! 🎁\n\n🍺 🍾 🍻 🍸 🍹</b>"
        else:
            if(task[2].trim()!=""):
                schedule_message = "<b>✨ Сегодня "+task[1]+" у "+task[2]+"! ✨\n\n🎆 Поздравляем! 🎆</b>"
            else:
                schedule_message = "<b>📢 Сегодня "+task[1]+"! 📢</b>"

        #print(schedule_message)
        await bot.send_message(chat_id=config.group_id.get_secret_value(), text=schedule_message,  parse_mode=ParseMode.HTML)

    await session.close()

if __name__ == '__main__':
    asyncio.run(send_schedule())
