from flask import Blueprint, render_template, request, session, current_app
from lab5 import db_connect, db_close  

lab6 = Blueprint('lab6', __name__)

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.get_json()
    req_id = data['id']
    method = data['method']

    conn, cur = db_connect()

    if method == 'info':
        cur.execute("SELECT number, tenant, price FROM offices ORDER BY number;")
        rows = cur.fetchall()
        offices = [dict(row) for row in rows]

        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': req_id
        }

    login = session.get('login')
    if not login:
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Пользователь не авторизован'
            },
            'id': req_id
        }

    if method == 'booking':
        office_number = data['params']

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute(
                "SELECT tenant FROM offices WHERE number = %s;",
                (office_number,)
            )
        else:
            cur.execute(
                "SELECT tenant FROM offices WHERE number = ?;",
                (office_number,)
            )

        row = cur.fetchone()
        if not row:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32601,
                    'message': 'Офис не найден'
                },
                'id': req_id
            }

        tenant = row['tenant']

        if tenant != '':
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Офис уже занят'
                },
                'id': req_id
            }

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute(
                "UPDATE offices SET tenant = %s WHERE number = %s;",
                (login, office_number)
            )
        else:
            cur.execute(
                "UPDATE offices SET tenant = ? WHERE number = ?;",
                (login, office_number)
            )

        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': 'Офис успешно забронирован',
            'id': req_id
        }

    if method == 'cancellation':
        office_number = data['params']

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute(
                "SELECT tenant FROM offices WHERE number = %s;",
                (office_number,)
            )
        else:
            cur.execute(
                "SELECT tenant FROM offices WHERE number = ?;",
                (office_number,)
            )

        row = cur.fetchone()
        if not row:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32601,
                    'message': 'Офис не найден'
                },
                'id': req_id
            }

        tenant = row['tenant']

        if tenant == '':
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Офис уже свободен'
                },
                'id': req_id
            }

        if tenant != login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'Вы не можете снять чужую аренду'
                },
                'id': req_id
            }

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute(
                "UPDATE offices SET tenant = '' WHERE number = %s;",
                (office_number,)
            )
        else:
            cur.execute(
                "UPDATE offices SET tenant = '' WHERE number = ?;",
                (office_number,)
            )

        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': 'Аренда успешно снята',
            'id': req_id
        }

    db_close(conn, cur)
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Неизвестный метод'
        },
        'id': req_id
    }
