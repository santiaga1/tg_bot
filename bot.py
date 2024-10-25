import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Get config from .env
from config_reader import config
# Bot handlers
from handlers import common, tasks, other


async def main():
    # Log bot info
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Dispatcher
    dp = Dispatcher(storage=MemoryStorage())
    # Bot object (bot token from .env)
    bot = Bot(config.bot_token.get_secret_value())

    # Routers
    dp.include_router(common.router)
    dp.include_router(tasks.router)
    dp.include_router(other.router)

    # Start polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
