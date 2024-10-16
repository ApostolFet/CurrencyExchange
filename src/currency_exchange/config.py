from dataclasses import dataclass
from pathlib import Path
from tomllib import load


@dataclass
class Config:
    host: str
    port: int


def load_config(path: Path = Path("config.example.toml")) -> Config:
    with path.open("rb") as file:
        data = load(file)
    config = Config(**data.get("server", {}))
    return config
