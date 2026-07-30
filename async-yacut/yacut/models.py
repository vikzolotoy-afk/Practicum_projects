from datetime import datetime, timezone

from yacut import db
from .constants import MAX_SHORT_LEN


class URLMap(db.Model):  # type: ignore
    """Модель для хранения URL-адресов."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(MAX_SHORT_LEN), unique=True, nullable=False)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=lambda: datetime.now(timezone.utc)
    )

    @staticmethod
    def exists(short_id):
        """Проверить, существует ли уже такой идентификатор."""
        if short_id == 'files':
            return True
        return URLMap.query.filter_by(short=short_id).first() is not None
