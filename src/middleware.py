from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware, Bot
from aiogram.types import CallbackQuery, Message, TelegramObject
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from auth import authenticateUser


class MyMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        if not (isinstance(event, Message | CallbackQuery)):
            return
        if event.from_user is None:
            return

        bot: Bot = data["bot"]
        engine: Engine = data["engine"]

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

            data["session"] = session
            data["user"] = user_result.user
            return await handler(event, data)
