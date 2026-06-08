from datetime import datetime


def generate_invoice(user, subscription):
    return {
        "invoice_id": f"INV-{int(datetime.utcnow().timestamp())}",
        "user_email": user.email,
        "plan": subscription.plan,
        "amount": 499,
        "currency": "INR",
        "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    }
