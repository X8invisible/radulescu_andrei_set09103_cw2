from flask import Flask, redirect , url_for, render_template, abort, request
import bcrypt
import sqlite3
import dataManager as dbManager
app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')
@app.route('/webhook/')
def webh():
    return render_template('webhook.html')
@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        username = request.form['username']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        dbManager.signUp(username, password)
        return redirect('/')
    else:
        return render_template('signup.html')
@app.route('/login', methods=['POST', 'GET'])
def log():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if dbManager.checkLogIn(username, password):
            return('good boi')
        else:
            return('bad boi')
    else:
        return render_template('signup.html')
@app.route('/logout')
def logout():
    return redirect('/')
if __name__=="__main__":
    app.run(host='localhost', debug=True)
