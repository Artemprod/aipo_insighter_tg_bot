import asyncio
import nats
from nats.aio.msg import Msg

from domain.enteties.message_enteties import IncomeTranscribedText


def listen(server, queue):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            nc = await nats.connect(server)
            await nc.subscribe(queue, cb=func)
            await nc.flush()
            print("Listening for results...")
            await asyncio.Future()  # Бесконечное ожидание, пока не будет отменено

        return wrapper

    return decorator


@listen(server="nats://demo.nats.io:4222", queue="foo")
async def received_result(msg: Msg):
    print(f"Received result: {msg.data.decode()}")
    a = IncomeTranscribedText.parse_raw(msg.data)
    return int(a.id_text)


if __name__ == '__main__':
    asyncio.run(received_result())
