import asyncio
import logging
import sys
from threading import Thread

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import (
    BotCommand,
)

from middleware import MyMiddleware
from routers import router as main_router
from routers.admin import router as admin_router
from routers.device import router as device_router
from settings import Settings
from wstunnel import start_wstunnel_server


dp = Dispatcher()
for event_observer in [dp.message, dp.callback_query]:
    event_observer.middleware(MyMiddleware())
dp.include_routers(
    admin_router,
    device_router,
    main_router,
)


async def main() -> None:
    settings = Settings.model_validate({})

    wstunnel_thread = Thread(target=start_wstunnel_server, args=(settings,))
    wstunnel_thread.start()

    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="devices", description="Список устройств"),
            BotCommand(command="add_device", description="Добавить устройство"),
            BotCommand(command="help", description="Помощь"),
        ]
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
