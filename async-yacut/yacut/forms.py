from flask_wtf import FlaskForm  # type: ignore
from wtforms import (  # type: ignore
    MultipleFileField,
    StringField,
    SubmitField,
    URLField,
)
from wtforms.validators import (  # type: ignore
    DataRequired,
    Length,
    Optional,
    Regexp,
)

from .constants import MAX_ORIGINAL_LEN, MAX_SHORT_LEN, SHORT_ID_REGEX


class URLMapForm(FlaskForm):
    """Форма для генерации коротких ссылок."""

    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(
                max=MAX_ORIGINAL_LEN,
                message=(
                    'Ссылка слишком длинная '
                    f'(максимум {MAX_ORIGINAL_LEN} символов)'
                )
            )
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(
                max=MAX_SHORT_LEN,
                message=(
                    f'Максимальная длина ссылки — '
                    f'{MAX_SHORT_LEN} символов'
                )
            ),
            Regexp(
                SHORT_ID_REGEX,
                message='Можно использовать только латинские буквы и цифры'
            )
        ]
    )
    submit = SubmitField('Создать')


class FilesForm(FlaskForm):
    """Форма для массовой загрузки файлов."""

    files = MultipleFileField(
        'Выберите файлы для загрузки',
        validators=[
            DataRequired(message='Необходимо выбрать хотя бы один файл')
        ]
    )
    submit = SubmitField('Загрузить на Яндекс Диск')
