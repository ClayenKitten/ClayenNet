from aiogram import F, Bot, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.orm import Session

from num_emoji import num_to_emoji_str
from schema import Device, User
from settings import Settings


router = Router()


@router.message(Command("help"))
@router.callback_query(F.data == "help")
async def help(
    event: Message | CallbackQuery,
    bot: Bot,
    *,
    user: User,
) -> None:
    if isinstance(event, CallbackQuery):
        await event.answer()
    await bot.send_message(
        user.tg_user_id,
        "\n".join(
            [
                "<b>Как подключить VPN?</b>",
                "1. Установите приложение WireGuard по ссылке ниже",
                "2. Добавьте устройство к своему аккаунту",
                "3. Скачайте файл настройки",
                "4. Зайдите в приложение WireGuard и подключите файл",
                "5. Запустите VPN",
            ]
        ),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📲 Windows",
                        url="https://download.wireguard.com/windows-client/wireguard-installer.exe",
                    ),
                    InlineKeyboardButton(
                        text="📲 macOS",
                        url="https://apps.apple.com/us/app/wireguard/id1451685025",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="📲 Android",
                        url="https://play.google.com/store/apps/details?id=com.wireguard.android",
                    ),
                    InlineKeyboardButton(
                        text="📲 iOS",
                        url="https://itunes.apple.com/us/app/wireguard/id1441195209?ls=1&mt=8",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="➕ Добавить новое устройство", callback_data="dev:new"
                    )
                ],
            ]
        ),
    )


@router.message()
async def default(_: Message, bot: Bot, *, user: User, settings: Settings) -> None:
    await send_main_menu(bot=bot, user=user, settings=settings)


async def send_main_menu(bot: Bot, user: User, settings: Settings):
    keyboard: list[list[InlineKeyboardButton]] = []

    keyboard.append(
        [
            InlineKeyboardButton(text="💻 Устройства", callback_data="dev:list"),
            InlineKeyboardButton(text="📖 Помощь", callback_data="help"),
        ]
    )
    if user.tg_username == settings.telegram_admin_username:
        keyboard.append(
            [InlineKeyboardButton(text="👑 Админ-панель", callback_data="admin")]
        )

    await bot.send_message(
        user.tg_user_id,
        "\n".join(["<b>ClayenNet</b>", "VPN функционирует штатно ✅"]),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )
