from flask import Flask, redirect , url_for, render_template, abort, request
import bcrypt
import sqlite3
app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')
@app.route('/webhook/')
def webh():
    return render_template('webhook.html')

if __name__=="__main__":
    app.run(host='localhost', debug=True)
