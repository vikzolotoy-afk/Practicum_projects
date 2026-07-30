from http import HTTPStatus

from flask import jsonify, render_template, request

from . import app, db
from .exceptions import InvalidAPIUsage


def is_api_request():
    """Проверить, является ли текущий запрос обращением к API."""
    return request.path.startswith('/api/')


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    """Вернуть JSON или HTML-страницу при ошибке 404."""
    if is_api_request():
        return (
            jsonify({'message': 'Указанный id не найден'}),
            HTTPStatus.NOT_FOUND
        )
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    """Обработать внутреннюю ошибку сервера."""
    db.session.rollback()
    if is_api_request():
        return (
            jsonify({'message': 'Внутренняя ошибка сервера'}),
            HTTPStatus.INTERNAL_SERVER_ERROR
        )
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
