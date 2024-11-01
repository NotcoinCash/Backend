import hashlib
import time
from typing import Annotated
from urllib.parse import parse_qs

from fastapi import Header, HTTPException


async def check_auth_header(Authentication: Annotated[str, Header()]):
    init_data = Authentication.split("\n")[1]
    init_data = parse_qs(init_data)

    bot_token = init_data.get('bot', [None])[0]
    if not bot_token:
        raise HTTPException(status_code=500, detail="Bot token is not set")

    hash_value = init_data.get('hash', [None])[0]
    if not hash_value:
        raise HTTPException(status_code=400, detail="Hash is missing from initData")
    init_data.pop('hash', None)

    auth_date = init_data.get('auth_date', [None])[0]
    if not auth_date:
        raise HTTPException(status_code=400, detail="auth_date is missing from initData")

    auth_timestamp = int(auth_date)
    current_timestamp = int(time.time())
    time_difference = current_timestamp - auth_timestamp
    five_minutes_in_seconds = 5 * 60
    if time_difference > five_minutes_in_seconds:
        raise HTTPException(status_code=400, detail="Telegram data is older than 5 minutes")

    data_check_string = '\n'.join(
        f"{key}={value[0]}" for key, value in sorted(init_data.items())
    )

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hashlib.sha256(secret_key + data_check_string.encode()).hexdigest()

    if calculated_hash != hash_value:
        raise HTTPException(status_code=400, detail="Invalid hash")
