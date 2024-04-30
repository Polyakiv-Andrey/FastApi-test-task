from datetime import timedelta, datetime

import jwt
from src.config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        access_token_expire: timedelta = settings.auth_jwt.access_token_expire,
        refresh_token_expire: timedelta = settings.auth_jwt.refresh_token_expire
) -> dict:
    now = datetime.utcnow()

    access_token_payload = payload.copy()
    access_token_payload.update(type="access_token", exp=now + access_token_expire, iat=now)
    access_token = jwt.encode(access_token_payload, private_key, algorithm=algorithm)

    refresh_token_payload = payload.copy()
    refresh_token_payload.update(type="refresh_token", exp=now + refresh_token_expire, iat=now)
    refresh_token = jwt.encode(refresh_token_payload, private_key, algorithm=algorithm)

    return {"access_token": access_token, "refresh_token": refresh_token}


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=algorithm
    )

    return decoded