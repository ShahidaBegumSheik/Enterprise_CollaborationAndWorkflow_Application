from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="Mini Enterprise Collaboration Flow", alias="APP_NAME")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = Field(
        default="mysql+pymysql://root:root@127.0.0.1:3306/ec",
        alias="DATABASE_URL",
    )

    jwt_secret: str = Field(default="change_me", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_minutes: int = Field(default=60*24*7, alias="REFRESH_TOKEN_EXPIRE_MINUTES")

    cors_origins: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173",
        alias="CORS_ORIGIN",
    )

    seed_admin: bool = Field(default=True, alias="SEED_ADMIN")
    admin_email: str = Field(default="admin@gmail.com", alias="ADMIN_EMAIL")
    admin_password: str = Field(default="admin1234", alias="ADMIN_PASSWORD")

    upload_dir: str = Field(default="uploads", alias="UPLOAD_DIR")
    max_upload_size_bytes: int = Field(default=5 * 1024 * 1024, alias="MAX_UPLOAD_SIZE_BYTES")

    rate_limit_login: str = Field(default="5/minute", alias="RATE_LIMIT_LOGIN")
    rate_limit_ticket_create: str = Field(default="10/hour", alias="RATE_LIMIT_TICKET_CREATE")

    razorpay_key_id: str = Field(default="", alias="RAZORPAY_KEY_ID")
    razorpay_key_secret: str = Field(default="", alias="RAZORPAY_KEY_SECRET")
    razorpay_webhook_secret: str = Field(default="", alias="RAZORPAY_WEBHOOK_SECRET")
    razorpay_pro_amount: int = Field(default=499, alias="RAZORPAY_PRO_AMOUNT")
    razorpay_currency: str = Field(default="INR", alias="RAZORPAY_CURRENCY")
    razorpay_company_name: str = Field(
        default="VertexCore", alias="RAZORPAY_COMPANY_NAME"
    )
    razorpay_company_description: str = Field(
        default="Enterprise Software", alias="RAZORPAY_COMPANY_DESCRIPTION"
    )

    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    cache_ttl_seconds: int = Field(default=60, alias="CACHE_TTL_SECONDS")

    google_client_id: str | None = None
    google_client_secret: str | None = None
    google_redirect_uri: str | None = None

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_dir).resolve()


settings = Settings()
