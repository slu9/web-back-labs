from flask import Flask, request
import datetime
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4

app = Flask (__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)

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
    <link rel="stylesheet" href="{{ url_for('static', filename='lab1/main.css') }}">
</head>
<body>
    <header>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <hr>
    </header>
    <main>
        <ol>
            <li><a href="/lab1">Первая лабораторная работа</a></li>
            <li><a href="/lab2">Вторая лабораторная работа</a></li>
            <li><a href="/lab3">Третья лабораторная работа</a></li>
            <li><a href="/lab4">Четвертая лабораторная работа</a></li>
        </ol>
    </main>
    <footer>
        &copy; Зырянова Софья Сергеевна, ФБИ-34, 3 курс, 2025
        <hr>
    </footer>
</body>
</html>
'''

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
