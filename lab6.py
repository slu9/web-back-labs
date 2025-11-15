from flask import Blueprint, render_template, request, session

lab6 = Blueprint('lab6', __name__)

offices = []
for i in range(1, 11):
    offices.append({"number": i, "tenant": "", "price": 1000})


@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.get_json()     
    req_id = data['id']
    method = data['method']

    if method == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': req_id
        }

    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': req_id
        }


    if method == 'booking':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Офис уже занят'
                        },
                        'id': req_id
                    }

                office['tenant'] = login
                return {
                    'jsonrpc': '2.0', 
                    'result': 'success',
                    'id': req_id
                }

    if method == 'cancellation':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] == '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Офис свободен'
                        },
                        'id': req_id
                    }
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Вы не можете снять чужую аренду'
                        },
                        'id': req_id
                    }
                office['tenant'] = ''
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': req_id
                }

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Странная ошибка'
        },
        'id': req_id
    }