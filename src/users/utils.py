import hashlib
import hmac


def hmac_sha256(key, message):
    return hmac.new(
        key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
