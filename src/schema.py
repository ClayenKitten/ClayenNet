from ipaddress import IPv4Network, ip_network
from sqlalchemy import BigInteger, ForeignKey, MetaData, Text, TypeDecorator, func
from sqlalchemy.dialects.postgresql import CIDR, INET
from sqlalchemy.orm import Mapped, mapped_column, registry
from uuid import UUID, uuid4


def uuid_column():
    return mapped_column(
        primary_key=True, default_factory=uuid4, server_default=func.gen_random_uuid()
    )


class IPNetworkType(TypeDecorator):
    impl = CIDR

    def process_bind_param(self, value, dialect):
        return str(value) if value else None

    def process_result_value(self, value, dialect):
        return IPv4Network(value) if value else None


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


reg = registry(
    metadata=MetaData(naming_convention=convention), type_annotation_map={str: Text()}
)


@reg.mapped_as_dataclass(kw_only=True)
class User:
    """User model representing a VPN user."""

    __tablename__ = "users"

    id: Mapped[UUID] = uuid_column()
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str | None] = mapped_column()
    tg_user_id: Mapped[int] = mapped_column(unique=True, type_=BigInteger())
    tg_username: Mapped[str] = mapped_column(unique=True)
    network: Mapped[IPv4Network] = mapped_column(unique=True, type_=IPNetworkType)


@reg.mapped_as_dataclass(kw_only=True)
class Invite:
    """Invite model for tracking Telegram username invitations."""

    __tablename__ = "invites"

    id: Mapped[UUID] = uuid_column()
    tg_username: Mapped[str] = mapped_column(unique=True)
    network: Mapped[IPv4Network] = mapped_column(unique=True, type_=IPNetworkType)


@reg.mapped_as_dataclass(kw_only=True)
class Device:
    """Device model representing a user's VPN-connected device."""

    __tablename__ = "devices"

    id: Mapped[UUID] = uuid_column()
    name: Mapped[str] = mapped_column(doc="Human-readable name of the device.")
    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey(User.id), doc="User that the device is associated with."
    )
    address: Mapped[str] = mapped_column(
        doc="Internal address of the device inside VPN network."
    )
    private_key: Mapped[str] = mapped_column(unique=True)
    public_key: Mapped[str] = mapped_column(unique=True)
