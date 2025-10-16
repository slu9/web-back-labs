from flask import Blueprint, url_for, request, redirect, Response, render_template
import datetime
lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a')
def a():
    return 'без слэша'

@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = [
    {"name": "роза", "price": 300},
    {"name": "тюльпан", "price": 310},
    {"name": "незабудка", "price": 320},
    {"name": "ромашка", "price": 330},
]

@lab2.route('/lab2/flowers/<int:flower_id>', methods=['GET'])
def flowers(flower_id):
    if not (0 <= flower_id < len(flower_list)):
        abort(404)
    f = flower_list[flower_id]
    return render_template('flower_info.html', flower=f, flower_id=flower_id)

@lab2.route('/lab2/flowers/', methods=['GET'])
def list_flowers():
    return render_template('flowers.html', flowers=flower_list)

@lab2.route('/lab2/add_flower', methods=['GET'])
def add_flower():
    name = (request.args.get("name") or "").strip()
    price_raw = (request.args.get("price") or "").strip()

    price_norm = price_raw.replace('+', '').replace(' ', '')
    if not name or not price_norm.isdigit():
        return ('<h1>400 Bad Request</h1>'
                '<p>Нужно ввести название и целую неотрицательную цену</p>'), 400

    flower_list.append({"name": name, "price": int(price_norm)})
    return redirect(url_for('list_flowers'))

@lab2.route('/lab2/del_flower/<int:flower_id>', methods=['GET'])
def del_flower(flower_id):
    if 0 <= flower_id < len(flower_list):
        flower_list.pop(flower_id)
        return redirect(url_for('list_flowers'))
    abort(404)

@lab2.route('/lab2/flowers/clear', methods=['GET'])
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('list_flowers'))

@lab2.route('/lab2/example')
def example():
        name = 'Зырянова Софья'
        number = '2'
        group = 'ФБИ-34'
        course = '3'
        fruits = [
            {'name': 'яблоки', 'price': 100},
            {'name': 'груши', 'price': 120},
            {'name': 'апельсины', 'price': 80},
            {'name': 'мандарины', 'price': 95},
            {'name': 'манго', 'price': 321}
        ]
        return render_template('example.html', name=name, number=number, group=group, course=course, fruits=fruits)

@lab2.route('/lab2/')
def lb2():
    return render_template('lab2.html')

@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a,b):
    return f'''
<!Doctype html>
<html>
    <body>
     <h1>Расчёт с параметрами:</h1>
     <ul>
        <li>{a} + {b} = {a + b}</li>
        <li>{a} - {b} = {a - b}</li>
        <li>{a} * {b} = {a * b}</li>
        <li>{a} / {b} = {'деление на 0' if b == 0 else a / b}</li>
        <li>{a}<sup>{b}</sup> = {a ** b}</li>
    </ul>
    </body>
</html>
'''

@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>')
def calc_one_arg(a):
    return redirect(f'/lab2/calc/{a}/1')

books = [
    {"title": "1984", "author": "Джордж Оруэлл", "genre": "Антиутопия", "pages": 328},
    {"title": "Маленький принц", "author": "Антуан де Сент-Экзюпери", "genre": "Сказка", "pages": 96},
    {"title": "Улисс", "author": "Джеймс Джойс", "genre": "Модернизм", "pages": 730},
    {"title": "Сто лет одиночества", "author": "Габриэль Гарсиа Маркес", "genre": "Магический реализм", "pages": 417},
    {"title": "Фауст", "author": "Иоганн Вольфганг Гёте", "genre": "Драма", "pages": 448},
    {"title": "Алхимик", "author": "Пауло Коэльо", "genre": "Притча", "pages": 208},
    {"title": "Над пропастью во ржи", "author": "Джером Сэлинджер", "genre": "Роман", "pages": 277},
    {"title": "Цветы для Элджернона", "author": "Дэниел Киз", "genre": "Фантастика", "pages": 320},
    {"title": "Гарри Поттер и философский камень", "author": "Джоан Роулинг", "genre": "Фэнтези", "pages": 352},
    {"title": "Имя розы", "author": "Умберто Эко", "genre": "Исторический детектив", "pages": 640}
]
@lab2.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

furniture = [
    {"name": "Диван",         "desc": "Мягкий трёхместный диван для гостиной.",             "image": "sofa.webp"},
    {"name": "Кресло",        "desc": "Уютное кресло с подлокотниками.",                   "image": "armchair.webp"},
    {"name": "Обеденный стол","desc": "Деревянный стол на 6 человек.",                     "image": "dining_table.avif"},
    {"name": "Стул",          "desc": "Классический стул с мягким сиденьем.",              "image": "chair.webp"},
    {"name": "Кровать",       "desc": "Двуспальная кровать с изголовьем.",                 "image": "bed.webp"},
    {"name": "Тумбочка",      "desc": "Прикроватная тумба с ящиками.",                     "image": "nightstand.jpg"},
    {"name": "Шкаф",          "desc": "Двухстворчатый шкаф для одежды.",                   "image": "wardrobe.webp"},
    {"name": "Комод",         "desc": "Низкий комод с четырьмя ящиками.",                  "image": "dresser.webp"},
    {"name": "Письменный стол","desc": "Рабочий стол для учёбы или офиса.",                "image": "desk.webp"},
    {"name": "Компьютерный стул","desc": "Эргономичное кресло на колёсиках.",             "image": "computer_chair.webp"},
    {"name": "Кухонный гарнитур","desc": "Модули для кухни с полками.",                    "image": "kitchen.jpg"},
    {"name": "Полка",         "desc": "Настенная полка для книг.",                          "image": "shelf.webp"},
    {"name": "Туалетный столик","desc": "Столик с зеркалом и ящиками.",                    "image": "vanity.jpg"},
    {"name": "Пуф",           "desc": "Мягкий пуфик без спинки.",                          "image": "pouf.jpg"},
    {"name": "Журнальный столик","desc": "Низкий столик для гостиной.",                    "image": "coffee_table.jpg"},
    {"name": "Этажерка",      "desc": "Открытая конструкция для хранения мелочей.",        "image": "etagere.webp"},
    {"name": "Скамья",        "desc": "Узкое сиденье без спинки.",                         "image": "bench.jpg"},
    {"name": "Барный стул",   "desc": "Высокий стул для барной стойки.",                   "image": "bar_stool.webp"},
    {"name": "Кухонный остров","desc": "Центральный модуль кухни для готовки.",            "image": "kitchen_island.jpg"},
    {"name": "Стеллаж",       "desc": "Открытый шкаф для книг и хранения.",                "image": "bookcase.jpg"},
]

@lab2.route("/lab2/furniture")
def show_furniture():
    return render_template("furniture.html", items=furniture)
