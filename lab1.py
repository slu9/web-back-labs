from flask import Blueprint, url_for, request, redirect, Response
import datetime
lab1 = Blueprint('lab1', __name__)

@lab1.route("/lab1")
def lab():
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

@lab1.route("/lab1/web")
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

@lab1.route("/lab1/author")
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

@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@lab1.route('/lab1/image')
def image():
    path_img = url_for("static", filename="lab1/hamster.jpg")
    path_css = url_for("static", filename="lab1/lab1.css")
    
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

@lab1.route('/lab1/counter')
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

@lab1.route("/lab1/reset_counter")
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

@lab1.route("/lab1/created")
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

@lab1.route("/lab1/400")
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

@lab1.route("/lab1/401")
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

@lab1.route("/lab1/402")
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

@lab1.route("/lab1/403")
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

@lab1.route("/lab1/405")
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

@lab1.route("/lab1/418")
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

@lab1.route("/lab1/error")
def server_error():
    x = 1 / 0
    return str(x)
