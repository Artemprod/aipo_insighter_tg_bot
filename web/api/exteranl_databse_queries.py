import asyncio

import aiohttp
from aiohttp import ClientSession

from domain.enteties.message_enteties import TranscribedTextId


async def do_get_request(session: ClientSession, url: str, params: dict):
    async with session.get(url, params=params) as response:
        response_data = await response.json()
        return response_data


async def do_post_request(session: ClientSession, url: str, payload: dict):
    async with session.post(url, json=payload) as response:  # Используйте json=payload
        return response


async def do_youtube_transcribition(youtube_url):
    api = "api/start/start_process_from_youtube"
    host = 'http://127.0.0.1:9192/'
    url = f"{host}{api}"
    async with aiohttp.ClientSession() as session:
        res = await do_post_request(session=session, url=url, payload={'url': youtube_url})
    return res


async def get_transcribed_text(text_id):
    api = "api/results/get_transcribed_text"
    host = 'http://127.0.0.1:9192/'
    url = f"{host}{api}"
    async with aiohttp.ClientSession() as session:
        res = await do_get_request(session=session, url=url, params={'id_text': text_id})
    return res['text']


async def get_summary_text(text_id):
    api = "api/results/get_summary_text"
    host = 'http://127.0.0.1:9192/'
    url = f"{host}{api}"
    async with aiohttp.ClientSession() as session:
        res = await do_get_request(session=session, url=url, params={'id_text': text_id})
    return res


if __name__ == '__main__':
    async def main():
        task_tr_1 = get_transcribed_text(text_id=1)
        task_tr_2 = get_transcribed_text(text_id=2)
        task_tr_3 = get_transcribed_text(text_id=3)
        task_sam_1 = get_summary_text(text_id=1)
        task_sam_2 = get_summary_text(text_id=2)
        task_sam_3 = get_summary_text(text_id=3)
        res = await asyncio.gather(task_tr_1,
                                   task_tr_2,
                                   task_tr_3, task_sam_1, task_sam_2, task_sam_3, )
        for i in res:
            print(i)


    asyncio.run(main())
