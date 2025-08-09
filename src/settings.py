from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    # Telegram
    telegram_admin_username: str = Field()
    telegram_bot_token: str = Field()

    # Public connection
    public_host: str = Field()
    public_port: int = Field(default=51820)
    # Wireguard
    wg_address: str = Field()
    wg_private_key: str = Field()
    wg_public_key: str = Field()
    # WebSocket Tunnel
    ws_port: int = Field(default=8443)
    ws_password: str = Field()
    # Database
    postgres_host: str = Field(default="postgres")
    postgres_db: str = Field()
    postgres_user: str = Field()
    postgres_password: str = Field()
    # Other
    disable_masquerade: bool = Field(default=False)
