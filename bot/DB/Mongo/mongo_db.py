import datetime
import hashlib
import os
import random

from mongoengine import connect

from DB.Mongo.mongo_enteties import Assistant
from project_logging.loging_config import loguru_main_logger


class MongoORMConnection:
    def __init__(self, mongo,
                 system_type):
        if system_type == "local":
            connect(db=mongo.bd_name,
                    host=mongo.local_host,
                    port=int(mongo.local_port))
        elif system_type == "docker":
            connect(db=mongo.bd_name,
                    host=mongo.docker_host,
                    port=int(mongo.local_port))


class MongoAssistantRepositoryORM:
    MAX_ID_LENGTH = 10
    MIN_ID_LENGTH = 1


    @staticmethod
    def get_all_assistants():
        return Assistant.objects()

    @staticmethod
    def get_one_assistant(assistant_id: str):
        return Assistant.objects(assistant_id=assistant_id).get()

    def create_new_assistants(self, assistant: Assistant):
        as_id = self.generate_id()
        assistant.assistant_id = as_id
        assistant.created_at = datetime.datetime.now()
        try:
            assistant.save()
            loguru_main_logger.info("Сохранено")
            return as_id
        except Exception:
            loguru_main_logger.exception('что то пошло не так при создании нового асистента ')
            return False

    @staticmethod
    def update_assistant_fild(assistant_id, assistant_fild, new_value):
        assistant_object: Assistant = Assistant.objects(assistant_id=assistant_id).get()
        assistant_object[assistant_fild] = new_value
        try:
            assistant_object.save()
            return True
        except Exception:
            loguru_main_logger.exception('что то пошло не так при изменение нового поля ')
            return False

    @staticmethod
    def delete_assistant(assistant_id: str):
        assistant_object: Assistant = Assistant.objects(assistant_id=assistant_id).get()
        try:
            assistant_object.delete()
            loguru_main_logger.info("Удалено")
        except Exception as e:
            loguru_main_logger.exception('Ошибка удаления', e)

    @staticmethod
    def generate_id(length=MAX_ID_LENGTH):
        if length > MongoAssistantRepositoryORM.MAX_ID_LENGTH or length < MongoAssistantRepositoryORM.MIN_ID_LENGTH:
            loguru_main_logger.exception(ValueError)
            raise ValueError(f"Length must be between {MongoAssistantRepositoryORM.MIN_ID_LENGTH}"
                             f" and {MongoAssistantRepositoryORM.MAX_ID_LENGTH}")


        # Генерируем случайные байты
        random_bytes = os.urandom(16)

        # Создаем хеш объект SHA-256
        hash_object = hashlib.sha256(random_bytes)

        # Получаем хеш в виде шестнадцатеричной строки и усекаем ее до требуемой длины
        short_hash = hash_object.hexdigest()[:length]
        for _ in range(3):
            short_hash += str(random.randint(0, 9))
        return str(short_hash)


