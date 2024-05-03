from environs import Env
from logtail import LogtailHandler
from loguru import logger


def load_loguru():
    env: Env = Env()
    try:
        env.read_env('../deploy/.env')
    except Exception as e:
        print(e)
    logtail_source_token = env("LOGTAIL_INSIGHTER_ADMIN_SOURCE")
    logtail_handler = LogtailHandler(source_token=logtail_source_token)
    logger.add(
        logtail_handler,
        format="{message}",
        level="INFO",
        backtrace=False,
        diagnose=False,
    )
    return logger


loguru_main_logger = load_loguru()

