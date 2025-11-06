from pydantic.main import Field, BaseModel
from pathlib import Path


class Extractor:
    def __init__(self):
        pass

    def extract():
        pass


class WalkerOptions(BaseModel):
    duration: float = Field(default=1.0, description="Duration of the track")


class Walker:
    def __init__(self, path: str):
        directory: Path = Path(path)
        options: WalkerOptions = WalkerOptions()
