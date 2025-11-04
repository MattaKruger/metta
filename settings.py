from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    aucostic_api_key: str = Field(default="")
    listenbrainz_api_key: str = Field(default="")
    musicbrainz_api_key: str = Field(default="")
