import asyncio
import re

import aiohttp

MAX_ORIGINAL_LEN = 2048
MAX_SHORT_LEN = 16
AUTO_GENERATED_LEN = 6
SHORT_ID_CHARS = (
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '0123456789'
)

API_HOST = 'https://yandex.net'
API_VERSION = 'v1'

SHORT_ID_REGEX = re.compile(r'^[a-zA-Z0-9]+$')

YADISK_CONNECTION_ERRORS = (
    aiohttp.ClientError,
    asyncio.TimeoutError,
    ValueError,
)
