class NotForTelegramError(Exception):
    """Исключения, которые не должны отправляться в Telegram."""


class APIResponseError(Exception):
    """Ошибка при ответе API (статус не 200 или пустые данные)."""


class TelegramError(NotForTelegramError):
    """Ошибка при отправке сообщения в Telegram."""
