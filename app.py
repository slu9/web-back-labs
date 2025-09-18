from flask import Flask, url_for, request, redirect
import datetime
app = Flask (__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

@app.route("/")
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
        </html"""

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route('/lab1/image')
def image():
    css_path = url_for("static", filename="lab1.css")
    path = url_for("static", filename="hamster.jpg")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Хомяк</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''
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
