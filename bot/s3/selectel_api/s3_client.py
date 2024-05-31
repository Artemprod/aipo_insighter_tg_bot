import asyncio
from contextlib import asynccontextmanager

import aiofiles
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from environs import Env
from types_aiobotocore_s3.client import S3Client as S3ClientType

from bot.s3.selectel_api.StorageClient import SelStorage


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
            sel_client: SelStorage,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()
        self.sel_client = sel_client

    @asynccontextmanager
    async def get_client(self) -> S3ClientType:
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file_path: str):
        object_name = file_path.split("/")[-1]
        try:
            async with self.get_client() as client:
                async with aiofiles.open(file_path, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=await file.read(),
                    )
                print(f"File {object_name} uploaded to {self.bucket_name}")
        except ClientError as e:
            print(f"Error uploading file: {e}")

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                print(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            print(f"Error deleting file: {e}")

    async def download_file(self, object_name: str, destination_path: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                data = await response["Body"].read()
                async with aiofiles.open(destination_path, "wb") as file:
                    await file.write(data)
                print(f"File {object_name} downloaded to {destination_path}")
        except ClientError as e:
            print(f"Error downloading file: {e}")

    async def get_all_object(self):
        try:
            async with self.get_client() as client:
                response = await client.list_objects_v2(Bucket=self.bucket_name)
                if 'Contents' in response:
                    return [obj['Key'] for obj in response['Contents']]
                return []
        except ClientError as e:
            print(f"Error listing objects: {e}")
            return []

    async def get_bucket_access_control_list(self):
        try:
            async with self.get_client() as client:
                response = await client.get_bucket_acl(Bucket=self.bucket_name)
                return response
        except ClientError as e:
            print(f"Error getting bucket ACL: {e}")
            return None

    async def get_object_link(self, Key: str):
        try:
            container_domen = await self.sel_client.get_pubdomains()
            return f"https://{container_domen[0].get('uuid')}.selstorage.ru/{Key}"
        except ClientError as e:
            print(f"Error getting object link: {e}")
            return None


async def main():
    env = Env()
    env.read_env('.env')

    username = env('SELECTEL_USERNAME')
    password = env('SELECTEL_PASSWORD')
    account_id = env('SELECTEL_ACCOUNT_ID')
    project_name = 'My First Project'
    bucket_name = 'public-insighter-1'

    sel_client = SelStorage(
        account_id=account_id,
        project_name=project_name,
        username=username,
        password=password,
        bucket_name=bucket_name,
    )
    s3_client = S3Client(
        access_key=env("S3_ACCESS_KEY"),
        secret_key=env("S3_SECRET_KEY"),
        endpoint_url="https://s3.storage.selcloud.ru",
        bucket_name="public-insighter-1",
        sel_client=sel_client,
    )
    print(await s3_client.get_object_link("posting-label-58515541-0006-2.pdf"))


if __name__ == "__main__":
    asyncio.run(main())
