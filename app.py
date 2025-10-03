from flask import Flask, url_for, request, redirect, Response, abort, render_template
import datetime
app = Flask (__name__)

visit_log = []

@app.errorhandler(404)
def not_found(err):
    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    
    visit_log.append({
        "ip": client_ip,
        "time": access_time,
        "url": requested_url
    })
    
    log_html = ""
    for entry in reversed(visit_log[-10:]): 
        log_html += f"<tr><td>{entry['ip']}</td><td>{entry['time']}</td><td>{entry['url']}</td></tr>"
    
    return f'''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>404 — Страница не найдена</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; padding: 20px; }}
        h1 {{ font-size: 50px; color: #cc0000; }}
        table {{ margin: 20px auto; border-collapse: collapse; width: 80%; }}
        th, td {{ border: 1px solid #999; padding: 8px; }}
        th {{ background-color: #f2f2f2; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>404 — Страница не найдена</h1>
    <p>Ваш IP: {client_ip}</p>
    <p>Дата и время доступа: {access_time}</p>
    <p><a href="/">Вернуться на главную</a></p>
    
    <h2>Последние посещения</h2>
    <table>
        <tr><th>IP</th><th>Дата и время</th><th>Запрошенный адрес</th></tr>
        {log_html}
    </table>
</body>
</html>
''', 404

@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>НГТУ, ФБ, Лабораторные работы</title>
</head>
<body>
    <header>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <hr>
    </header>
    <main>
        <ol>
            <li><a href="/lab1">Первая лабораторная</a></li>
        </ol>
    </main>
    <footer>
        &copy; Зырянова Софья Сергеевна, ФБИ-34, 3 курс, 2025
        <hr>
    </footer>
</body>
</html>
'''
@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Лабораторная 1</title>
</head>
<body>
    <h1>Лабораторная работа 1</h1>
    <p>
        Flask — фреймворк для создания веб-приложений на языке программирования Python, 
        использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. 
        Относится к категории так называемых микрофреймворков — минималистичных 
        каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
    </p>

    <a href="/">На главную</a>

    <h2>Список роутов</h2>
    <ul>
        <li><a href="/lab1/image">/lab1/image</a></li>
        <li><a href="/lab1/counter">/lab1/counter</a></li>
        <li><a href="/lab1/author">/lab1/author</a></li>
        <li><a href="/lab1//reset_counter">/lab1/reset_counter</a></li>
        <li><a href="/lab1/created">/lab1/created</a></li>
        <li><a href="/lab1/400">/lab1/400</a></li>
        <li><a href="/lab1/401">/lab1/401</a></li>
        <li><a href="/lab1/402">/lab1/402</a></li>
        <li><a href="/lab1/403">/lab1/403</a></li>
        <li><a href="/lab1/405">/lab1/405</a></li>
        <li><a href="/lab1/418">/lab1/418</a></li>
        <li><a href="/lab1/error">/lab1/error</a></li>
    </ul>
</body>
</html>
'''

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
           </body>
        </html>""", 200, {
            "X-Server": "sample",
            'Content-Type':'text/plan; charset=utf-8'
            }

@app.route("/lab1/author")
def author():
    name = "Зырянова Софья Сергеевна"
    group = "ФБИ-34"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body>
        </html>
        """

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route('/lab1/image')
def image():
    path_img = url_for("static", filename="hamster.jpg")
    path_css = url_for("static", filename="lab1.css")
    
    html = f'''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Хомяк</title>
    <link rel="stylesheet" href="{path_css}">
</head>
<body>
    <h1>Хомяк</h1>
    <img src="{path_img}" alt="Хомяк">
</body>
</html>
'''
    headers = {
        "Content-Language": "ru",
        "X-Author": "Zyryanova_Sofya", 
        "X-Lab": "Lab1"
    }
    
    return Response(html, status=200, headers=headers)

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        <a href="/reset_counter">Сбросить счётчик</a>
    </body>
</html>
'''
@app.route("/reset_counter")
def reset_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        <h1>Счётчик сброшен!</h1>
        <a href="/counter">Вернуться к счётчику</a>
    </body>
</html>
'''

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i>
    </body>
</html>
''', 201

@app.route("/lab1/400")
def bad_request():
    return '''
<!doctype html>
<html>
    <body>
        <h1>400 — Bad Request</h1>
        <p>Некорректный запрос.</p>
    </body>
</html>
''', 400

@app.route("/lab1/401")
def unauthorized():
    return '''
<!doctype html>
<html>
    <body>
        <h1>401 — Unauthorized</h1>
        <p>Требуется авторизация.</p>
    </body>
</html>
''', 401

@app.route("/lab1/402")
def payment_required():
    return '''
<!doctype html>
<html>
    <body>
        <h1>402 — Payment Required</h1>
        <p>Необходима оплата для доступа.</p>
    </body>
</html>
''', 402

@app.route("/lab1/403")
def forbidden():
    return '''
<!doctype html>
<html>
    <body>
        <h1>403 — Forbidden</h1>
        <p>Доступ запрещён.</p>
    </body>
</html>
''', 403

@app.route("/lab1/405")
def method_not_allowed():
    return '''
<!doctype html>
<html>
    <body>
        <h1>405 — Method Not Allowed</h1>
        <p>Метод не разрешён для этого ресурса.</p>
    </body>
</html>
''', 405

@app.route("/lab1/418")
def teapot():
    return '''
<!doctype html>
<html>
    <body>
        <h1>418 — I'm a teapot</h1>
        <p>Я чайник.</p>
    </body>
</html>
''', 418

@app.route("/lab1/error")
def server_error():
    x = 1 / 0
    return str(x)

@app.errorhandler(500)
def internal_error(err):
    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>500 — Внутренняя ошибка сервера</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
        }
        h1 {
            font-size: 60px;
            color: #cc0000;
        }
        p {
            font-size: 20px;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>500</h1>
    <p>Произошла внутренняя ошибка сервера</p>
    <a href="/">Вернуться на главную</a>
</body>
</html>
''', 500

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)

    name = flower_list[flower_id]
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Информация о цветке</h1>
    <p><b>ID:</b> {flower_id}</p>
    <p><b>Название:</b> {name}</p>
    <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
    </body>
</html>
'''

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/example')
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

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/add_flower/')
def add_flower_missing():
    return '''
<!doctype html>
<html>
    <body>
        <h1>400 Bad request</h1>
        <p>вы не задали имя цветка</p>
    </body>
</html>
''', 400

@app.route('/lab2/flowers/')
def list_flowers():
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Список цветов</h1>
        <p>Всего цветов: {len(flower_list)}</p>
        <ul>
            {''.join(f'<li>{flower}</li>' for flower in flower_list) or '<li>Список пуст</li>'}
        </ul>
    </body>
</html>
'''

@app.route('/lab2/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return '''
<!doctype html>
<html>
    <body>
        <h1>Список цветов очищен</h1>
        <p>Все цветы удалены из списка</p>
        <p><a href="/lab2/flowers">Перейти к списку всех цветов</a></p></p>
    </body>
</html>
'''
