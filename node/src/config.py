from dataclasses import dataclass
import os

class Configuration:
    def __init__(self):
        api_password = os.getenv("API_PASSWORD")
        if api_password is None:
            raise RuntimeError("Environment variable API_PASSWORD must be set")
        self.api_password = api_password

        self.wg_interface = os.getenv("WG_INTERFACE", "wg0")

    api_password: str
    wireguard_interface: str
