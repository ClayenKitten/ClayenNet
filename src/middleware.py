from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware, Bot
from aiogram.types import CallbackQuery, Message, TelegramObject
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from auth import authenticateUser
from settings import Settings


class MyMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        bot: Bot = data["bot"]

        if not (isinstance(event, Message | CallbackQuery)):
            return
        if event.from_user is None:
            return

        # Workaround for typechecker, see https://github.com/pydantic/pydantic/issues/3753.
        settings = Settings.model_validate({})
        engine = create_engine(
            f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}/{settings.postgres_db}"
        )
        with Session(engine) as session:
            user_result = await authenticateUser(session, event.from_user)
            if user_result is None:
                await bot.send_message(event.from_user.id, "Доступ запрещён")
                return
            if user_result.is_new_user:
                await bot.send_message(
                    event.from_user.id,
                    "Добро пожаловать! Ваша учётная запись успешно создана.",
                )

            data["settings"] = settings
            data["engine"] = engine
            data["session"] = session
            data["user"] = user_result.user
            return await handler(event, data)
