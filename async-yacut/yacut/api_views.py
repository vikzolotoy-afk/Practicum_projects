from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .constants import MAX_SHORT_LEN, SHORT_ID_REGEX
from .exceptions import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id_api():
    """Создать короткую ссылку для переданного URL."""
    data = request.get_json(silent=True)

    if data is None:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса',
            HTTPStatus.BAD_REQUEST
        )

    if 'url' not in data or not data.get('url'):
        raise InvalidAPIUsage(
            '"url" является обязательным полем!',
            HTTPStatus.BAD_REQUEST
        )

    original_link = data.get('url')
    custom_id = data.get('custom_id')

    if custom_id:
        if (len(custom_id) > MAX_SHORT_LEN
                or not SHORT_ID_REGEX.match(custom_id)):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки',
                HTTPStatus.BAD_REQUEST
            )

        if URLMap.exists(custom_id):
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.',
                HTTPStatus.BAD_REQUEST
            )

        short_id = custom_id
    else:
        short_id = get_unique_short_id()

    url_map = URLMap(original=original_link, short=short_id)
    db.session.add(url_map)
    db.session.commit()

    return jsonify({
        'url': url_map.original,
        'short_link': url_for(
            'redirect_view',
            short_id=short_id,
            _external=True
        )
    }), HTTPStatus.CREATED


@app.route('/api/id/<path:path>/', methods=['GET'])
def get_original_url_api(path=None):
    """Вернуть оригинальный URL по его короткому идентификатору."""
    if not path:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    clean_id = path.strip('/')
    url_map = URLMap.query.filter_by(short=clean_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return jsonify({'url': url_map.original}), HTTPStatus.OK
