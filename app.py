from flask import Flask, render_template, request, redirect, url_for
import socket, time
from flask_sqlalchemy import SQLAlchemy


app = Flask("__name__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Regs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return '<Regs %r>' % self.id


# ниже главный чат /////////////////////////////////////////////////////////////////////////////////////


@app.route('/main', methods=['POST', 'GET'])
def main():
    login_test = request.args['login_test']

    

    return render_template("main.html", login=login_test)


# ниже регистрация //////////////////////////////////////////////////////////////////////////////////////


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']

        test = Regs.query.filter_by(login=login).first()
        
        if test is not None:
            if login == test.login:
                return ("Такой логин уже существует")
        else: 
            regs = Regs(login=login, password=password)

            try:
                db.session.add(regs)
                db.session.commit()
                return redirect('/login')
            except:
                return ("Ошибка хз какая, но она точно не появится")
    else:
        return render_template('registration.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        login_test = request.form['login']
        password_test = request.form['password']
        try:
            test = Regs.query.filter_by(login=login_test).first()

            if login_test == test.login and password_test == test.password:
                # return redirect('/main')
                return redirect(url_for('.main', login_test=login_test))
            else:
                return ("Неверный пароль")
        except:
            return ("Логин не существует")

    else:
        return render_template("login.html")


# ниже прелюдия к проекту ////////////////////////////////////////////////////////////////////////////////////


@app.get("/")
def loading():
    return render_template("loading.html")


@app.route("/calculator", methods=['POST', 'GET'])
def calculator():
    global x1
    if x1 == '228':
        x1 = ''
        return redirect("/login")
    else:
        return render_template("calc.html", x = x1, sign = sign1, y = y1) 

    
@app.route("/counting", methods=['POST', 'GET'])
def counting():
    global x1, sign1, y1

    digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
    action = ['-', '+', 'x', '/', '%']
    
    tmp = request.form['index']
    if tmp in digit and sign1 == '':
        x1 += tmp
    if tmp in action and x1 != '':
        sign1 = tmp
    if tmp in digit and sign1 != '':
        y1 += tmp
    if tmp == 'ac':
        x1 = ''
        sign1 = ''
        y1 = ''
    if tmp == '=':
        if sign1 == '%':
            if y1 == '0':
                x1 = 'Ты идиот?'
            else:
                x1 = float(x1) % float(y1)
        if sign1 == '/':
            if y1 == '0':
                x1 = 'Ты идиот?'
            else:
                x1 = float(x1) / float(y1)
        if sign1 == 'x':
            x1 = float(x1) * float(y1)
        if sign1 == '-':
            x1 = float(x1) - float(y1)
        if sign1 == '+':
            x1 = float(x1) + float(y1)
        y1 = ''
        sign1 = ''

    return redirect("/calculator")


global x1, sign1, y1
x1 = ''
sign1 = ''
y1 = ''
