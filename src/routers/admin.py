from aiogram import F, Bot, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from schema import Device, User
from settings import Settings
from wg_server import start_wg_server


router = Router()


@router.callback_query(F.data == "admin")
async def admin(
    callback: CallbackQuery,
    bot: Bot,
    *,
    user: User,
    settings: Settings,
    session: Session,
) -> None:
    if user.tg_username != settings.telegram_admin_username:
        await callback.answer("Доступ запрещён")
        return

    users = session.execute(select(User)).scalars()

    text = "<b>👑 Админ-панель</b>\n\n<b>👨‍👩‍👦 Пользователи</b>"
    for i, user_ in enumerate(users):
        devices_count = session.execute(
            select(func.count("*")).where(Device.owner_id == user_.id).select_from()
        ).scalar_one()
        text += f"\n{i+1}. @{user_.tg_username} ({devices_count} устройств)"

    await bot.send_message(
        user.tg_user_id,
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔁 Обновить", callback_data="admin:refresh"
                    )
                ]
            ]
        ),
    )
    await callback.answer()


@router.callback_query(F.data == "admin:refresh")
async def admin_refresh(
    callback: CallbackQuery,
    *,
    user: User,
    settings: Settings,
    session: Session,
) -> None:
    if user.tg_username != settings.telegram_admin_username:
        await callback.answer("Доступ запрещён")
        return
    try:
        start_wg_server(settings, session)
    except Exception as err:
        await callback.answer(f"Ошибка\n\n{err}", True)

    await callback.answer("Успешно")
