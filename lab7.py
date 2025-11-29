from flask import Blueprint, render_template, request

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films = [
    {
        "title": "Materialists",
        "title_ru": "Материалистка",
        "year": 2025,
        "description": "Люси, лучшая сотрудница нью-йоркского брачного агентства, "
        "мастерски составляет пары, но сама ни с кем не встречается в уверенности, что выйдет замуж "
        "только за очень богатого. Однажды на свадьбе клиентов Люси знакомится с братом жениха, мужчиной во всех "
        "отношениях приятным и к тому же миллионером, и в этот самый момент в её жизнь возвращается бывший "
        "парень — актёр-неудачник, которого она бросила из-за проблем с деньгами."
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

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def fet_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Фильм с таким id не найден"}, 404

    return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Фильм с таким id не найден"}, 404
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Фильм с таким id не найден"}, 404
    film = request.get_json()
    films[id] = film
    return films[id]

@lab7.route('/lab7/rest-api/films', methods=['POST'])
def add_film():
    new_film = request.get_json()
    films.append(new_film)
    new_id = len(films) - 1
    return {"id": new_id}, 201
