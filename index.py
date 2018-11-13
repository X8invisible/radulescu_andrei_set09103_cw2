from flask import Flask, redirect , url_for, render_template, abort, request, session, flash
import bcrypt
import sqlite3
import ConfigParser
import dataManager as dbManager
app = Flask(__name__)

def init(app):
    config = ConfigParser.ConfigParser()
    try:
        config_location = "etc/defaults.cfg"
        config.read(config_location)

        app.config['DEBUG'] = config.get("config", "debug")
        app.config['ip_address'] = config.get("config", "ip_address")
        app.config['port'] = config.get("config", "port")
        app.config['url'] = config.get("config", "url")
        app.config['SECRET_KEY'] = config.get("config", "SECRET_KEY")
    except:
        print "Could not read config from: ", config_location

@app.route('/')
def root():
    try:
        if(session['name']):
            logged = True
            name = session['name']
    except KeyError:
            logged = False
            name = "Account"
            pass
    return render_template('index.html', logged = logged, name = name, title = "Home")
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
        return render_template('signup.html', logged = False, name = "Account", title = "Sign Up")
@app.route('/login', methods=['POST', 'GET'])
def log():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if dbManager.checkLogIn(username, password):
            session['name'] = username
            return redirect('/')
        else:
            return('bad boi')
    else:
        try:
            if(session['name']):
                logged = True
                name = session['name']
                flash('You are already Logged In! ')
        except KeyError:
                logged = False
                name = "Account"
                pass
        return render_template('signup.html', logged = logged, name = name, title = "Log In")
@app.route('/profile/')
def dashboard():
    return render_template('profile.html', logged = False, name = "Account", title = "Dashboard")
@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect('/')

app.secret_key = app.config['SECRET_KEY']
if __name__=="__main__":
    init(app)
    app.run(
        host = app.config['ip_address'],
        port = int(app.config['port']),
        debug = app.config['DEBUG']
    )
