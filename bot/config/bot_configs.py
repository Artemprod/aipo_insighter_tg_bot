from dataclasses import dataclass
from typing import Union

from environs import Env


@dataclass
class AdminTelegramBot:
    tg_bot_token: str
    telegram_server_url: str


@dataclass
class MongoDB:
    bd_name: str
    # для пользования на локальной машине
    local_port: int
    local_host: Union[int, str]
    # для пользования на сервере в доккере
    docker_port: int
    docker_host: Union[int, str]


@dataclass
class RedisStorage:
    # для пользования на локальной машине

    admin_bot_local_port: int
    admin_bot_local_host: Union[int, str]
    # для пользования на сервере в доккере

    admin_bot_docker_port: int
    admin_bot_docker_host: Union[int, str]


@dataclass
class SystemType:
    system_type: str


@dataclass
class S3Config:
    access_key: str
    secret_key: str


@dataclass
class Config:
    # data_base: MongoDB
    # redis_storage: RedisStorage
    AdminBot: AdminTelegramBot
    # system: SystemType
    s3_config: S3Config


def load_bot_config(path) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        AdminBot=AdminTelegramBot(
            tg_bot_token=env('BOT_TOKEN'),
            telegram_server_url=env('TELEGRAM_SERVER_URL')
        ),
        s3_config=S3Config(
            access_key=env('S3_ACCESS_KEY'),
            secret_key=env('S3_SECRET_KEY')
        )
    )
