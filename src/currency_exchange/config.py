from dataclasses import dataclass
from pathlib import Path
from tomllib import load


@dataclass
class Config:
    host: str
    port: int
    allow_origins: list[str]
    allow_methods: list[str]
    allow_headers: list[str]
    allow_credentials: bool


def load_config(path: Path = Path("config.example.toml")) -> Config:
    with path.open("rb") as file:
        data = load(file)
    config = Config(**data.get("server", {}))
    return config
