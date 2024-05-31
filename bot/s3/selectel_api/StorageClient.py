from contextlib import asynccontextmanager
from typing import Type, Optional

from aioselectel_api import SelectelStorageClient
from aioselectel_api.client import get_token


class SelStorage:
    """Класс для работы с Selectel Storage
    Если у вас есть токен, передайте его в параметре keystone_token
    тогда не будет генерироваться новый токен
    :param account_id: str ID вашего аккаунта
    :param project_name: str имя проекта
    :param username: str имя пользователя
    :param password: str пароль
    :param bucket_name: str имя бакета
    :param keystone_token: Optional[str] токен для авторизации
    """

    def __init__(self,
                 account_id: str,
                 project_name: str,
                 username: str,
                 password: str,
                 bucket_name: str,
                 keystone_token: Type[Optional[str]] = None):
        self.account_id = account_id
        self.project_name = project_name
        self.username = username
        self.password = password
        self.bucket_name = bucket_name
        self.keystone_token = keystone_token

    @asynccontextmanager
    async def get_client(self) -> SelectelStorageClient:
        if not self.keystone_token:
            token = self.keystone_token = await get_token(
                username=self.username,
                password=self.password,
                account_id=self.account_id,
                project_name=self.project_name
            )
        async with SelectelStorageClient(keystone_token=self.keystone_token, container_name=self.bucket_name) as client:
            yield client

    async def get_pubdomains(self) -> dict:
        async with self.get_client() as client:
            client: SelectelStorageClient
            return await client.get_pubdomains()
