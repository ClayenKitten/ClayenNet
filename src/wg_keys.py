import codecs
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives import serialization


def create_wg_private_key() -> str:
    private_key = X25519PrivateKey.generate()
    bytes_ = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return codecs.encode(bytes_, "base64").decode("utf8").strip()


def create_wg_public_key(private_key: str) -> str:
    bytes_ = codecs.decode(private_key.encode("utf-8"), "base64")
    private_key_ = X25519PrivateKey.from_private_bytes(bytes_)
    pubkey = private_key_.public_key().public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    )
    return codecs.encode(pubkey, "base64").decode("utf8").strip()
