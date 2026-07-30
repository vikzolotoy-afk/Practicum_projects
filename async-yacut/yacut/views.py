from flask import flash, redirect, render_template, request, url_for

from . import app, db
from .forms import FilesForm, URLMapForm
from .models import URLMap
from .utils import get_unique_short_id, run_async_upload


@app.route("/", methods=['GET', 'POST'])
def index_view():
    """Обрабатывать главную страницу и создавать короткие ссылки."""
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        original_link = form.original_link.data

        if custom_id:
            if URLMap.exists(custom_id):
                flash(
                    'Предложенный вариант короткой ссылки уже существует.',
                    'validation-error'
                )
                return render_template('index.html', form=form), 200
            short_id = custom_id
        else:
            short_id = get_unique_short_id()

        url_map = URLMap(original=original_link, short=short_id)
        db.session.add(url_map)
        db.session.commit()

        short_url = url_for('redirect_view', short_id=short_id, _external=True)
        return (
            render_template('index.html', form=form, short_url=short_url),
            200,
        )

    return render_template('index.html', form=form), 200


@app.route("/files", methods=['GET', 'POST'])
def files_view():
    """Обрабатывать загрузку файлов и генерацию коротких ссылок."""
    form = FilesForm()
    uploaded_files = []

    if request.method == 'POST':
        files = request.files.getlist('files')
        valid_files = [f for f in files if f.filename]

        if valid_files:
            upload_results = run_async_upload(valid_files)

            for result in upload_results:
                filename = result['filename']
                download_url = result['download_url']
                short_id = get_unique_short_id()
                url_map = URLMap(original=download_url, short=short_id)
                db.session.add(url_map)
                uploaded_files.append(
                    {
                        'name': filename,
                        'short_url': url_for(
                            'redirect_view',
                            short_id=short_id,
                            _external=True,
                        ),
                    }
                )

            db.session.commit()
            return (
                render_template('500.html', form=form, files=uploaded_files),
                200,
            )

    return render_template('500.html', form=form), 200


@app.route('/<string:short_id>')
def redirect_view(short_id):
    """Перенаправить пользователя по оригинальной ссылке."""
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
