from pydantic import BaseModel, ConfigDict


class SubscriptionOut(BaseModel):
    id: int
    organization_id: int
    plan: str
    status: str
    credits: int
    max_users: int
    max_storage_mb: int
    amount: int
    provider: str | None = None
    razorpay_order_id: str | None = None
    razorpay_payment_id: str | None = None
    razorpay_subscription_id: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RazorpayOrderOut(BaseModel):
    order_id: str
    key_id: str
    amount: int
    currency: str
    company_name: str
    description: str


class VerifyPaymentIn(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
