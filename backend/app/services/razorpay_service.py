import hashlib
import hmac

import razorpay

from app.core.config import settings


def get_client():
    if not settings.razorpay_key_id or not settings.razorpay_key_secret:
        raise RuntimeError("Razorpay credentials are missing in .env")
    return razorpay.Client(
        auth=(settings.razorpay_key_id, settings.razorpay_key_secret)
    )


def create_order(amount: int | None = None):
    client = get_client()
    payload = {
        "amount": amount or settings.razorpay_pro_amount,
        "currency": settings.razorpay_currency,
        "payment_capture": 1,
    }
    return client.order.create(data=payload)


def verify_payment_signature(order_id: str, payment_id: str, signature: str) -> bool:
    generated = hmac.new(
        settings.razorpay_key_secret.encode(),
        f"{order_id}|{payment_id}".encode(),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(generated, signature)


def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    generated = hmac.new(
        settings.razorpay_webhook_secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(generated, signature)
