import hashlib
import time
from typing import Annotated
from urllib.parse import parse_qs

from fastapi import Header, HTTPException

from src.config import settings
from src.users import utils


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
    five_minutes_in_seconds = 5 * 60
    if time_difference > five_minutes_in_seconds:
        raise HTTPException(status_code=400, detail="Telegram data is older than 5 minutes")

    data_check_string = "\n".join(f"{key}={value[0]}" for key, value in sorted(init_data.items()))
    secret_key = utils.hmac_sha256(settings.SECRET_KEY, "WebAppData")

    calculated_hash = utils.hmac_sha256(data_check_string, secret_key)
    print('\n'*5)
    print(data_check_string)

    print(secret_key)
    print(calculated_hash)
    print('\n' * 5)

    if calculated_hash != hash_value:
        raise HTTPException(status_code=400, detail="Invalid hash")
