from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5433
    POSTGRES_DB: str

    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRES_AT: int = 60 * 24
    ALGORITHM: str = "HS256"
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    SECRET_KEY: str = "super secret key"
    FRONTEND_URL: str = "http://localhost:5173"

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field
    @property
    def OAUTH2_PROVIDERS(self) -> dict:
        return {
            "google": {
                "client_id": self.GOOGLE_CLIENT_ID,
                "client_secret": self.GOOGLE_CLIENT_SECRET,
                "authorize_url": "https://accounts.google.com/o/oauth2/auth",
                "token_url": "https://accounts.google.com/o/oauth2/token",
                "userinfo": {
                    "url": "https://www.googleapis.com/oauth2/v3/userinfo",
                    "email": lambda json: json["email"],
                },
                "scopes": ["https://www.googleapis.com/auth/userinfo.email"],
            },
            "github": {
                "client_id": self.GITHUB_CLIENT_ID,
                "client_secret": self.GITHUB_CLIENT_SECRET,
                "authorize_url": "https://github.com/login/oauth/authorize",
                "token_url": "https://github.com/login/oauth/access_token",
                "userinfo": {
                    "url": "https://api.github.com/user/emails",
                    "email": lambda json: json[0]["email"],
                },
                "scopes": ["user:email"],
            },
        }


settings = Settings()
