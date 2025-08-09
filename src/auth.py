from collections import namedtuple
from dataclasses import dataclass
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from schema import Invite, User
from aiogram.types import User as TgUser


@dataclass
class UserResult:
    user: User
    is_new_user: bool


async def authenticateUser(session: Session, tg_user: TgUser) -> UserResult | None:
    query = select(User).where(User.tg_user_id == tg_user.id)
    user = session.execute(query).scalar_one_or_none()

    if user is not None:
        return UserResult(user=user, is_new_user=False)

    if tg_user.username is None:
        return None

    # Check invites
    invite = session.execute(
        delete(Invite)
        .where(Invite.tg_username == tg_user.username)
        .returning(Invite.network)
    ).first()
    if invite is None:
        return None
    user = User(
        tg_user_id=tg_user.id,
        tg_username=tg_user.username,
        first_name=tg_user.first_name,
        last_name=tg_user.last_name,
        network=invite[0],
    )
    session.add(user)
    session.commit()
    return UserResult(user=user, is_new_user=True)
