from flask import Flask, render_template, request, redirect
import socket, time

app = Flask("__name__")



@app.route("/main", methods=['POST', 'GET'])
def main():
    return render_template("main.html")



@app.route("/login", methods=['POST', 'GET'])
def login():
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
    #return render_template("calc.html", x = x1, sign = sign1, y = y1)

global x1, sign1, y1
x1 = ''
sign1 = ''
y1 = ''
