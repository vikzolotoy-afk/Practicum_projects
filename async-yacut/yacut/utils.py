import asyncio
from http import HTTPStatus
import random
import re
from urllib.parse import urljoin

import aiohttp
from flask import current_app

from .constants import (
    API_HOST,
    API_VERSION,
    AUTO_GENERATED_LEN,
    SHORT_ID_CHARS,
    YADISK_CONNECTION_ERRORS,
)
from .models import URLMap


def get_unique_short_id():
    """Генерировать уникальный короткий идентификатор."""
    while True:
        short_id = ''.join(
            random.choices(SHORT_ID_CHARS, k=AUTO_GENERATED_LEN)
        )
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


async def upload_single_file(session, file_bytes, filename, token):
    """Асинхронно загружать файл на Яндекс Диск."""
    auth_headers = {'Authorization': f'OAuth {token}'}
    base_api_url = urljoin(API_HOST, f'{API_VERSION}/')
    upload_url_api = urljoin(base_api_url, 'disk/resources/upload')
    params = {'path': f'/{filename}', 'overwrite': 'true'}

    try:
        async with session.get(
            upload_url_api,
            headers=auth_headers,
            params=params
        ) as response:
            if response.status != HTTPStatus.OK:
                return None
            data = await response.json()
            upload_url = data.get('href')

        if upload_url:
            if 'yandex' not in upload_url:
                upload_url = re.sub(
                    r'^https?://[^/]+',
                    API_HOST.rstrip('/'),
                    upload_url
                )

            async with session.put(
                upload_url, headers={}, data=file_bytes
            ) as put_response:
                if put_response.status not in (
                    HTTPStatus.CREATED,
                    HTTPStatus.ACCEPTED,
                    HTTPStatus.OK
                ):
                    return None

                download_url_api = urljoin(
                    base_api_url, 'disk/resources/download'
                )
                download_params = {'path': f'/{filename}'}

                async with session.get(
                    download_url_api,
                    headers=auth_headers,
                    params=download_params
                ) as dl_response:
                    if dl_response.status == HTTPStatus.OK:
                        dl_data = await dl_response.json()
                        return dl_data.get('href')
    except YADISK_CONNECTION_ERRORS:
        return None
    return None


async def upload_files_to_disk(files_list):
    """Загрузить список файлов на диск."""
    token = current_app.config['DISK_TOKEN']
    if not token:
        return []

    results = []
    async with aiohttp.ClientSession() as session:
        for file in files_list:
            file_bytes = file.read()
            filename = file.filename

            download_url = await upload_single_file(
                session, file_bytes, filename, token
            )
            if download_url:
                results.append({
                    'filename': filename,
                    'download_url': download_url
                })

        return results


def run_async_upload(files_list):
    """Выполняет синхронный запуск асинхронной загрузки файлов."""
    return asyncio.run(upload_files_to_disk(files_list))


async def download_file_from_disk_async(api_url, token):
    """Асинхронно скачивает бинарный файл с Яндекс Диска."""
    auth_headers = {'Authorization': f'OAuth {token}'}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url, headers=auth_headers) as response:
                if response.status == HTTPStatus.OK:
                    return await response.read()
        except YADISK_CONNECTION_ERRORS:
            return None
    return None
