import re


async def validate_youtube_url(url):
    # Шаблоны URL, которые поддерживают список видео, короткие ссылки и стандартные ссылки
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'  # YouTube видео всегда имеют 11-значный ID
    )

    return bool(re.match(youtube_regex, url))
