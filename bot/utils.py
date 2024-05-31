import requests

from bot.config.bot_configs import load_bot_config

config = load_bot_config('.env')
TOKEN = config.AdminBot.tg_bot_token
API_URL = 'http://localhost:8081/bot' + TOKEN
TELEGRA_URL = 'https://api.telegram.org/bot' + TOKEN


async def get_file_url(file_id) -> str:
    response = requests.get(f"{TELEGRA_URL}/getFile?file_id={file_id}")
    print(response.url)
    result = response.json()

    if response.status_code == 200:
        file_path = result['result']['file_path']
        return file_path
    else:
        raise Exception("Error getting file URL")


def download_file(file_url, destination):
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception("Error downloading file")


if __name__ == '__main__':
    # Пример использования:
    file_id = 'YOUR_FILE_ID'  # Замените на актуальный file_id
    file_url = get_file_url(file_id)
    download_file(file_url, 'downloaded_file.ext')  # Замените 'downloaded_file.ext' на нужное имя файла
