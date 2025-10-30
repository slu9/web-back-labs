from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4')
def lab(): 
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if not x1 or not x2:
        return render_template('div.html', error="Введите оба числа!")

    x1 = float(x1)
    x2 = float(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error="Ошибка: деление на ноль невозможно!")

    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum_():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    x1 = x1.strip() if x1 else ''
    x2 = x2.strip() if x2 else ''

    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0

    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    x1 = x1.strip() if x1 else ''
    x2 = x2.strip() if x2 else ''

    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1

    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if not x1 or not x2 or x1.strip() == '' or x2.strip() == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow_():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if not x1 or not x2 or x1.strip() == '' or x2.strip() == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)

    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='0 в степени 0 не определено!')

    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count 

    if request.method == 'POST':
        operation = request.form.get('operation')

        if operation == 'plant' and tree_count < 10:
            tree_count += 1
        elif operation == 'cut' and tree_count > 0:
            tree_count -= 1

    return render_template('lab4/tree.html', tree_count=tree_count)

users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Кузнецов', 'gender': 'm'},
    {'login': 'bob', 'password': '555', 'name': 'Борис Федоров', 'gender': 'm'},
    {'login': 'sofya', 'password': '111', 'name': 'Софья Зырянова', 'gender': 'f'},
    {'login': 'kate', 'password': '222', 'name': 'Екатерина Комкина', 'gender': 'f'},
]

@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab4/login.html', authorized=False)
    
    login_value = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()
    
    if login_value == '':
        return render_template('lab4/login.html', authorized=False, error='Не введен логин', login_value=login_value)
    
    if password == '':
        return render_template('lab4/login.html', authorised=False, login_value=login_value)
    
    for user in users:
        if login_value == user['login'] and password == user['password']:
            session['user_name'] = user['name']
            session['gender'] = user['gender']
            return render_template('lab4/login.html', authorized=True, user_name=user['name'])
        
    return render_template('lab4/login.html', error="Неверные логин и/или пароль", authorized=False, login_value=login_value)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = None
    snowflakes = 0
    temp_value = ''

    if request.method == 'POST':
        temp = request.form.get('temp', '').strip()
        temp_value = temp  

        if temp == '':
            message = 'ошибка: не задана температура'
        else:
            try:
                t = int(temp)
            except ValueError:
                message = 'ошибка: температура должна быть числом'
            else:
                if t < -12:
                    message = 'не удалось установить температуру — слишком низкое значение'
                elif t > -1:
                    message = 'не удалось установить температуру — слишком высокое значение'
                elif -12 <= t <= -9:
                    message = f'Установлена температура: {t}°С'
                    snowflakes = 3
                elif -8 <= t <= -5:
                    message = f'Установлена температура: {t}°С'
                    snowflakes = 2
                elif -4 <= t <= -1:
                    message = f'Установлена температура: {t}°С'
                    snowflakes = 1

    return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes, temp_value=temp_value)

@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    prices = {
        'barley': 12000,   
        'oats': 8500,      
        'wheat': 9000,     
        'rye': 15000       
    }

    message = None
    error = None
    discount_applied = False
    discount_amount = 0
    total = None
    weight_value = ''
    grain_value = 'barley' 

    if request.method == 'POST':
        grain_value = request.form.get('grain', 'barley')
        weight_str = request.form.get('weight', '').strip()
        weight_value = weight_str  

        if weight_str == '':
            error = 'Ошибка: не указан вес'
        else:
            try:
                weight = float(weight_str)
            except ValueError:
                error = 'Ошибка: вес должен быть числом'
            else:
                if weight <= 0:
                    error = 'Ошибка: вес должен быть больше 0'
                elif weight > 100:
                    error = 'Такого объёма сейчас нет в наличии'
                else:
                    price_per_ton = prices.get(grain_value, 0)
                    total = weight * price_per_ton

                    if weight > 10:
                        discount_applied = True
                        discount_amount = total * 0.10
                        total = total * 0.90

                    grain_names = {
                        'barley': 'ячмень',
                        'oats': 'овёс',
                        'wheat': 'пшеница',
                        'rye': 'рожь'
                    }
                    grain_human = grain_names.get(grain_value, 'зерно')

                    message = (
                        f'Заказ успешно сформирован. '
                        f'Вы заказали: {grain_human}. '
                        f'Вес: {weight} т. '
                        f'Сумма к оплате: {int(total)} руб.'
                    )

    return render_template(
        'lab4/grain.html', message=message, error=error, discount_applied=discount_applied, discount_amount=discount_amount, total=total, weight_value=weight_value, grain_value=grain_value)
