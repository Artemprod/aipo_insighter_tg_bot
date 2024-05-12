import asyncio
import nats
from nats.aio.msg import Msg

from domain.enteties.message_enteties import IncomeTranscribedText


# def listen(server, queue):
#     def decorator(func):
#         async def wrapper(*args, **kwargs):
#             nc = await nats.connect(server)
#             await nc.subscribe(queue, cb=func)
#             await nc.flush()
#             print("Listening for results...")
#             await asyncio.Future()  # Бесконечное ожидание, пока не будет отменено
#         return wrapper
#
#     return decorator
def listen(server, queue):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            nc = await nats.connect(server)

            future = asyncio.Future()  # Создаём объект Future для контроля завершения

            async def cb(msg):
                try:
                    # Вызываем декорируемую функцию с полученным сообщением
                    result = await func(msg, *args, **kwargs)
                    future.set_result(result)  # Устанавливаем результат для Future
                except Exception as e:
                    future.set_exception(e)  # Устанавливаем исключение, если что-то пошло не так

            await nc.subscribe(queue, cb=cb)
            await nc.flush()
            print("Listening for results...")

            return await future  # Ожидаем, пока Future не будет установлен и возвращаем результат

        return wrapper

    return decorator


@listen(server="nats://demo.nats.io:4222", queue="transcribe")
async def received_transcribed_id(msg: Msg):
    print(f"Received result: {msg.data.decode()}")
    a = IncomeTranscribedText.parse_raw(msg.data)
    # if int(a.id_text)>0:
    #     #answer[id_text) = 'SELECT TEXT WHERE id = id_text'
    #     #send message answer[id_text)
    # Отправить сообщение с тем что переволд закончени и фильтр на хэгдлер что перевод закончкен ( не запустаться при нескольких запросах )
    return int(a.id_text)

@listen(server="nats://demo.nats.io:4222", queue="summary")
async def received_summary_id(msg: Msg):
    print(f"Received result: {msg.data.decode()}")
    a = IncomeTranscribedText.parse_raw(msg.data)
    # if int(a.id_text)>0:
    #     #answer[id_text) = 'SELECT TEXT WHERE id = id_text'
    #     #send message answer[id_text)
    # Отправить сообщение с тем что переволд закончени и фильтр на хэгдлер что перевод закончкен ( не запустаться при нескольких запросах )
    return int(a.id_text)


if __name__ == '__main__':
    asyncio.run(received_transcribed_id())
