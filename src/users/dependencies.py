import hashlib
import hmac
import time
from typing import Annotated
from urllib.parse import parse_qs

from fastapi import Header, HTTPException

from src.config import settings


async def check_auth_header(Authentication: Annotated[str, Header()]):
    init_data = Authentication.split(" ")
    if len(init_data) != 2:
        raise HTTPException(status_code=400, detail="Invalid Authentication header")

    init_data = parse_qs(init_data[1])

    bot_token = settings.TELEGRAM_BOT_TOKEN
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
    one_hour = 60 * 60
    if time_difference > one_hour:
        # raise HTTPException(status_code=400, detail="Telegram data is older than 5 minutes")
        pass

    data_check_string = "\n".join(f"{key}={value[0]}" for key, value in sorted(init_data.items()))

    secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if calculated_hash != hash_value:
        raise HTTPException(status_code=400, detail="Invalid hash")

    telegram_id = init_data.get('id', None)
    return telegram_id
