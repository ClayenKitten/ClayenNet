import re
from sqlalchemy import select
from sqlalchemy.orm import Session
from schema import Device, User
from settings import Settings
from wg_keys import create_wg_private_key, create_wg_public_key
from wg_server import start_wg_server


async def add_device(
    *, settings: Settings, session: Session, user: User, name: str
) -> Device:
    if len(name) < 2 or len(name) > 16:
        raise InvalidDeviceName("Имя устройства должно иметь длину от 2 до 16 символов")
    if not re.match("^[a-zA-Zа-яА-ЯёЁ][a-zA-Zа-яА-ЯёЁ0-9 _-]+$", name):
        raise InvalidDeviceName(
            'Имя устройства должно начинаться с буквы и содержать только буквы, цифры, символы "_" и "-"'
        )

    devices = (
        session.execute(select(Device).where(Device.owner_id == user.id))
        .scalars()
        .all()
    )
    for address in user.network.hosts():
        if any(dev.address == str(address) for dev in devices):
            continue
        break
    else:
        raise UserNetworkExhausted()

    private_key = create_wg_private_key()
    public_key = create_wg_public_key(private_key)
    new_device = Device(
        name=name,
        owner_id=user.id,
        address=str(address),
        private_key=private_key,
        public_key=public_key,
    )
    session.add(new_device)
    session.commit()

    start_wg_server(settings, session)

    return new_device


class DeviceCreationException(Exception):
    pass


class InvalidDeviceName(DeviceCreationException):
    def __init__(self, message: str):
        self.message = message


class UserNetworkExhausted(DeviceCreationException):
    message = "Лимит устройств исчерпан, обратитесь к администратору."
