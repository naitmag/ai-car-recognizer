import asyncio

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot import config

from aiogram import Bot, Dispatcher
from bot.handlers import router

# Bot initiation
bot = Bot(
    config.SECRET_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)


async def main():
    dp = Dispatcher()

    # Register handlers
    dp.include_routers(
        router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print("[+]BOT STARTED")
    asyncio.run(main())
