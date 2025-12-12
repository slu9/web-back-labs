from flask import Blueprint, render_template, request, jsonify
from datetime import datetime 
import sqlite3

DB_PATH = 'films.db'
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS films (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                title_ru TEXT NOT NULL,
                year INTEGER NOT NULL,
                description TEXT NOT NULL
            )
        """)

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    init_db()
    return render_template('lab7/index.html')


films = [
    {
        "title": "Materialists",
        "title_ru": "Материалистка",
        "year": 2025,
        "description": "Люси, лучшая сотрудница нью-йоркского брачного агентства, "
                       "мастерски составляет пары, но сама ни с кем не встречается в уверенности, что выйдет замуж "
                       "только за очень богатого. Однажды на свадьбе клиентов Люси знакомится с братом жениха, мужчиной "
                       "во всех отношениях приятным и к тому же миллионером, и в этот самый момент в её жизнь "
                       "возвращается бывший парень — актёр-неудачник, которого она бросила из-за проблем с деньгами."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись"
                       " в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны"
                       " решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым"
                       " умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения."
    },
    {
        "title": "The Gentlemen",
        "title_ru": "Джентльмены",
        "year": 2019,
        "description": "Один ушлый американец ещё со студенческих лет приторговывал наркотиками, а теперь придумал схему"
                       " нелегального обогащения с использованием поместий обедневшей английской аристократии и очень неплохо на этом разбогател."
                       " Другой пронырливый журналист приходит к Рэю, правой руке американца, и предлагает тому купить киносценарий, в котором "
                       "подробно описаны преступления его босса при участии других представителей лондонского криминального мира — партнёра-еврея,"
                       " китайской диаспоры, чернокожих спортсменов и даже русского олигарха."
    },
]

def validate_and_normalize(data):
    errors = {}

    title_ru = (data.get('title_ru') or '').strip()
    title = (data.get('title') or '').strip()
    description = (data.get('description') or '').strip()
    year_raw = data.get('year')

    if not title_ru:
        errors['title_ru'] = 'Русское название обязательно'

    if title_ru and not title:
        title = title_ru

    current_year = datetime.now().year
    try:
        year = int(year_raw)
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть от 1895 до {current_year}'
    except (TypeError, ValueError):
        errors['year'] = 'Год должен быть числом'
        year = None


    if not description:
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'

    cleaned = {
        "title": title,
        "title_ru": title_ru,
        "year": year,
        "description": description
    }

    return errors, cleaned


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    with get_db() as conn:
        rows = conn.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id").fetchall()
    return jsonify([dict(r) for r in rows])

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, title, title_ru, year, description FROM films WHERE id = ?",
            (id,)
        ).fetchone()

    if row is None:
        return jsonify({"error": "Фильм с таким id не найден"}), 404

    return jsonify(dict(row))

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    data = request.get_json() or {}
    errors, film = validate_and_normalize(data)
    if errors:
        return jsonify(errors), 400

    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO films(title, title_ru, year, description) VALUES (?, ?, ?, ?)",
            (film["title"], film["title_ru"], film["year"], film["description"])
        )
        new_id = cur.lastrowid

    return jsonify({"id": new_id}), 201

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def update_film(id):
    data = request.get_json() or {}
    errors, film = validate_and_normalize(data)
    if errors:
        return jsonify(errors), 400

    with get_db() as conn:
        cur = conn.execute(
            "UPDATE films SET title=?, title_ru=?, year=?, description=? WHERE id=?",
            (film["title"], film["title_ru"], film["year"], film["description"], id)
        )

    if cur.rowcount == 0:
        return jsonify({"error": "Фильм с таким id не найден"}), 404

    return jsonify({"ok": True})


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    with get_db() as conn:
        cur = conn.execute("DELETE FROM films WHERE id = ?", (id,))

    if cur.rowcount == 0:
        return jsonify({"error": "Фильм с таким id не найден"}), 404

    return '', 204
