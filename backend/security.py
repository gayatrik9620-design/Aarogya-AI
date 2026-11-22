import os
import hashlib
import hmac
import jwt

from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.database import get_connection

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-local-secret-change-me")
ALGORITHM = "HS256"

bearer = HTTPBearer()


def hash_password(password):

    salt = os.urandom(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        180000
    )

    return salt.hex() + ":" + hashed.hex()


def verify_password(password, stored):

    try:
        salt, original_hash = stored.split(":")

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            bytes.fromhex(salt),
            180000
        ).hex()

        return hmac.compare_digest(new_hash, original_hash)

    except (ValueError, TypeError):
        return False


def create_access_token(user_id):

    expiry = datetime.now(timezone.utc) + timedelta(hours=12)

    return jwt.encode(
        {
            "sub": str(user_id),
            "exp": expiry
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer)
):

    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = int(payload["sub"])

    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    with get_connection() as conn:

        user = conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return dict(user)