from flask import Flask, redirect , url_for, render_template, abort, request, session, flash
from functools import wraps
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
def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        status = session.has_key('name')
        if not status:
            logged = False
            name = "Account"
            return redirect('/')
        return f(*args, **kwargs)
    return decorated
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
@app.route('/profile/<name>/')
@requires_login
def dashboard(name = None):
    if name == None:
        name = session['name']
        return render_template('profile.html', logged = True, name = name, title = "Dashboard")
    else:
        if dbManager.checkUserExists(name) and name == session['name']:
            return render_template('profile.html', logged = True, name = name, title = "Dashboard")
        else:
            abort(403)
@app.route('/webhook/add', methods=['POST', 'GET'])
@requires_login
def webh_add():
    if request.method=='POST':
        name = request.form['name']
        avatar = request.form['avatar']
        url = request.form['url']
        owner = dbManager.getUserId(session['name'])
        dbManager.addWebHook(name,avatar,url,owner)
        return redirect('/')
    return render_template('submitWebh.html', logged = True, name = session['name'], title = "New Webhook")
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
