from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # listenbrainz_api_key: str = Field(default="")
    # musicbrainz_api_key: str = Field(default="")

    aucoustic_api_key: str = Field(default="")

    last_fm_api_key: str = Field(default="")
    last_fm_secret: str = Field(default="")
    last_fm_user: str = Field(default="")
    last_fm_pass: str = Field(default="")
