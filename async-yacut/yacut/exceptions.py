from http import HTTPStatus


class InvalidAPIUsage(Exception):
    """Исключение для некорректных запросов к API."""

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        """Инициализировать ошибку сообщением и статус-кодом."""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Преобразовать ошибку в словарь для ответа API."""
        return dict(message=self.message)
