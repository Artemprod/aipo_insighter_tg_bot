from config.bot_configs import Config, load_bot_config
from DB.Mongo.mongo_db import MongoAssistantRepositoryORM, MongoORMConnection


config_data: Config = load_bot_config('.env')
MongoORMConnection(config_data.data_base, system_type=config_data.system.system_type)
assistant_repository = MongoAssistantRepositoryORM()


