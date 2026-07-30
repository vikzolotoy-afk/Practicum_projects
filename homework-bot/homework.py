import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telebot  # type: ignore
from dotenv import load_dotenv

from exceptions import APIResponseError, NotForTelegramError, TelegramError

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)


def check_tokens():
    """Проверить доступность переменных окружения."""
    tokens = {
        'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
    }
    missing = [name for name, value in tokens.items() if not value]
    if missing:
        logger.critical(f'Отсутствуют токены: {", ".join(missing)}')
        return False
    return True


def get_api_answer(timestamp):
    """Сделать запрос к единственному эндпоинту API-сервиса."""
    payload = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
    except requests.RequestException as error:
        raise APIResponseError(f'Сетевая ошибка при запросе к API: {error}')

    if response.status_code != HTTPStatus.OK:
        raise ValueError(
            f'Эндпоинт {ENDPOINT} недоступен. Код: {response.status_code}'
        )

    return response.json()


def check_response(response):
    """Проверить ответ API на соответствие документации."""
    if not isinstance(response, dict):
        raise TypeError('Ответ API не является словарем')
    if 'homeworks' not in response or 'current_date' not in response:
        raise KeyError('В ответе API отсутствуют ожидаемые ключи')
    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise TypeError('Под ключом homeworks пришел не список')
    return homeworks


def parse_status(homework):
    """Извлечь статус из информации о конкретной домашней работе."""
    name = homework.get('homework_name')
    status = homework.get('status')
    if not name or not status:
        raise KeyError('В ответе API нет имени работы или статуса')
    if status not in HOMEWORK_VERDICTS:
        raise ValueError(f'Неизвестный статус: {status}')
    verdict = HOMEWORK_VERDICTS[status]
    return f'Изменился статус проверки работы "{name}". {verdict}'


def send_message(bot, message):
    """Отправить сообщение в Telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except (telebot.apihelper.ApiTelegramException,
            requests.RequestException) as error:
        raise TelegramError(f'Сбой при отправке в Telegram: {error}')
    else:
        logger.debug(f'Сообщение отправлено: {message}')


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        sys.exit('Критическая ошибка: токены не найдены.')

    bot = telebot.TeleBot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    last_error = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)

            if homeworks:
                message = parse_status(homeworks[0])
                send_message(bot, message)
            else:
                logger.debug('Нет новых статусов')

            timestamp = response.get('current_date', timestamp)
            last_error = ''

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            if not isinstance(error, NotForTelegramError):
                if message != last_error:
                    try:
                        send_message(bot, message)
                        last_error = message
                    except Exception as send_error:
                        logger.error(
                            f'Даже сообщение об ошибке не ушло: {send_error}'
                        )

        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    main()
