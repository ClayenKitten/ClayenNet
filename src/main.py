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
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from middleware import MyMiddleware
from routers import router as main_router
from routers.admin import router as admin_router
from routers.device import router as device_router
from settings import Settings
from wg_server import start_wg_server
from wstunnel import start_wstunnel_server


async def main() -> None:
    # Workaround for typechecker, see https://github.com/pydantic/pydantic/issues/3753.
    settings = Settings.model_validate({})
    engine = create_engine(
        f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}/{settings.postgres_db}"
    )

    wstunnel_thread = Thread(target=start_wstunnel_server, args=(settings,))
    wstunnel_thread.start()

    with Session(engine) as session:
        start_wg_server(settings, session)

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
    dp = Dispatcher(settings=settings, engine=engine)
    dp.message.middleware(MyMiddleware())
    dp.callback_query.middleware(MyMiddleware())
    dp.include_routers(
        admin_router,
        device_router,
        main_router,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
