from re import Match
import re
from aiogram import F, Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    CopyTextButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.orm import Session

from num_emoji import num_to_emoji_str
from routers import send_main_menu
from schema import Device, User
from settings import Settings
from use_cases.device import (
    DeviceCreationException,
    InvalidDeviceName,
    UserNetworkExhausted,
    add_device,
)
from wg_config import print_wireguard_config
from wg_keys import create_wg_private_key, create_wg_public_key


router = Router()


@router.message(Command("devices"))
@router.callback_query(F.data == "dev:list")
async def devices(
    event: Message | CallbackQuery,
    bot: Bot,
    *,
    user: User,
    settings: Settings,
    session: Session,
) -> None:
    devices = (
        session.execute(select(Device).where(Device.owner_id == user.id))
        .scalars()
        .all()
    )

    builder = InlineKeyboardBuilder()
    for i, device in enumerate(devices):
        num = num_to_emoji_str(i + 1)
        builder.button(text=f"{num} {device.name}", callback_data=f"dev:{device.id}")
    builder.adjust(3)
    keyboard = builder.export()
    keyboard.append(
        [
            InlineKeyboardButton(
                text="➕ Добавить новое устройство", callback_data="dev:new"
            )
        ]
    )

    await bot.send_message(
        user.tg_user_id,
        (
            "<b>Мои устройства</b>\n"
            + "Выберите устройство из списка ниже, чтобы скачать файл настройки."
            if len(devices) > 0
            else 'Подключите устройство с помощью кнопки "Добавить".'
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )
    if isinstance(event, CallbackQuery):
        await event.answer()


class States(StatesGroup):
    awaiting_device_name = State()


@router.message(Command("add_device"))
@router.callback_query(F.data == "dev:new")
async def device_new_1(
    event: Message | CallbackQuery,
    state: FSMContext,
    bot: Bot,
    *,
    session: Session,
    user: User,
) -> None:
    devices = (
        session.execute(select(Device).where(Device.owner_id == user.id))
        .scalars()
        .all()
    )
    suggestions = filter(
        lambda suggestion: not any(dev.name == suggestion for dev in devices),
        ["Компьютер", "Ноутбук", "Телефон", "Планшет"],
    )

    await state.set_state(States.awaiting_device_name)
    if isinstance(event, CallbackQuery):
        await event.answer()

    await bot.send_message(
        user.tg_user_id,
        "\n".join(["Укажите имя устройства"]),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                list(
                    map(lambda suggestion: KeyboardButton(text=suggestion), suggestions)
                ),
                [KeyboardButton(text="Отмена")],
            ],
            is_persistent=True,
            resize_keyboard=True,
            input_field_placeholder="Имя устройства...",
        ),
    )


@router.message(States.awaiting_device_name)
async def device_new_2(
    message: Message,
    state: FSMContext,
    bot: Bot,
    *,
    user: User,
    session: Session,
    settings: Settings,
) -> None:
    if message.text is None:
        await message.answer("Укажите имя устройства")
        return

    if message.text == "Отмена":
        await message.answer(
            "Отмена создания устройства", reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
        await send_main_menu(bot, user, settings)
        return

    # Create device
    try:
        device = await add_device(
            settings=settings, session=session, user=user, name=message.text
        )
    except UserNetworkExhausted as err:
        await message.answer(err.message, reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return
    except InvalidDeviceName as err:
        await message.answer(err.message)
        return
    # Display result
    wg_config = print_wireguard_config(settings, device)
    await bot.send_document(
        chat_id=user.tg_user_id,
        document=BufferedInputFile(
            file=wg_config.encode("utf-8"), filename=f"{device.name}.conf"
        ),
        caption=f"🏘 IP адрес: <code>{device.address}</code>",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear()


@router.callback_query(F.data.regexp(r"^dev:(.+)$").as_("match"))
async def device(
    callback: CallbackQuery,
    match: Match[str],
    bot: Bot,
    *,
    user: User,
    settings: Settings,
    session: Session,
) -> None:
    device_id: str = match[1]

    device = session.execute(
        select(Device).where(Device.id == device_id).where(Device.owner_id == user.id)
    ).scalar_one_or_none()
    if device is None:
        await callback.answer("Устройство не найдено")
        return

    wg_config = print_wireguard_config(settings, device)

    await callback.answer()
    await bot.send_document(
        chat_id=user.tg_user_id,
        document=BufferedInputFile(
            file=wg_config.encode("utf-8"), filename=f"{device.name}.conf"
        ),
        caption=f"🏘 IP адрес: <code>{device.address}</code>",
        reply_markup=ReplyKeyboardRemove(),
    )
