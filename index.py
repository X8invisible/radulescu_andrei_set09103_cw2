from flask import Flask, redirect , url_for, render_template, abort, request, session, flash
from functools import wraps
import bcrypt
import sqlite3
import configparser
import dataManager as dbManager
app = Flask(__name__)
colorScheme="red"
def init(app):
    config = configparser.ConfigParser()
    try:
        config_location = "etc/defaults.cfg"
        config.read(config_location)

        app.config['DEBUG'] = config.get("config", "debug")
        app.config['ip_address'] = config.get("config", "ip_address")
        app.config['port'] = config.get("config", "port")
        app.config['url'] = config.get("config", "url")
        app.config['SECRET_KEY'] = config.get("config", "SECRET_KEY")
    except:
        print ("Could not read config from: ", config_location)
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
            colorScheme = dbManager.getColor(dbManager.getUserId(name))[0][0]
    except KeyError:
            logged = False
            name = "Account"
            colorScheme = "red"
            pass
    return render_template('index.html', logged = logged, name = name, title = "Home", color = colorScheme)
@app.route('/webhook/<webhId>')
@requires_login
def sendWebh(webhId = None):
    colorScheme = dbManager.getColor(dbManager.getUserId(session['name']))[0][0]
    webhooks = dbManager.getWebhookList(int(dbManager.getUserId(session['name'])))
    for webh in webhooks:
        if int(webh[4]) == int(webhId):
            return render_template('webhook.html', logged = True, name = session['name'], title = webh[0], webh = webh, color = colorScheme)
    abort(403)
@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        username = request.form['username']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        if(dbManager.checkUserExists(username)):
            flash('Username already exists!')
            return redirect('/signup')
        else:
            dbManager.signUp(username, password)
            return redirect('/')
    else:
        return render_template('signup.html', logged = False, name = "Account", title = "Sign Up", color = colorScheme)
@app.route('/login', methods=['POST', 'GET'])
def log():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if dbManager.checkLogIn(username, password):
            session['name'] = username
            return redirect('/')
        else:
            flash('Incorrect login')
            return redirect('/login')
    else:
        try:
            if(session['name']):
                logged = True
                name = session['name']
                colorScheme = dbManager.getColor(dbManager.getUserId(session['name']))[0][0]
                flash('You are already Logged In! ')
        except KeyError:
                logged = False
                name = "Account"
                colorScheme = "red"
                pass
        return render_template('signup.html', logged = logged, name = name, title = "Log In", color = colorScheme)
@app.route('/profile/', methods=['POST', 'GET'])
@app.route('/profile/<name>/', methods=['POST', 'GET'])
@requires_login
def dashboard(name = None):
    colorScheme = dbManager.getColor(dbManager.getUserId(session['name']))[0][0]
    if request.method=='POST':
        id = request.form.get('delete')
        dbManager.deleteWebhook(id)
        return redirect('/profile/')
    else:
        if name == None:
            name = session['name']
            userWebh = dbManager.getWebhookList(dbManager.getUserId(name))
            return render_template('profile.html', logged = True, name = name, title = "Dashboard", webhooks = userWebh, color = colorScheme)
        else:
            if dbManager.checkUserExists(name) and name == session['name']:
                userWebh = dbManager.getWebhookList(dbManager.getUserId(name))
                return render_template('profile.html', logged = True, name = name, title = "Dashboard", webhooks = userWebh, color = colorScheme)
            else:
                abort(403)
@app.route('/profile/edit', methods=['POST', 'GET'])
@requires_login
def edit_user():
    colorScheme = dbManager.getColor(dbManager.getUserId(session['name']))[0][0]
    if request.method=='POST':
        cScheme= request.form['scheme']
        passwordNew = request.form.get('passwordNew')
        passwordOld = request.form.get('passwordOld')
        if(passwordNew == ''):
            dbManager.editColor(session['name'], cScheme)
            colorScheme = cScheme
        else:
            if not dbManager.checkLogIn(session['name'], passwordOld):
                flash('Wrong old password!', 'alert-warning')
            else:
                password = bcrypt.hashpw(passwordNew.encode('utf-8'), bcrypt.gensalt())
                dbManager.editPassword(session['name'], password)
                dbManager.editColor(session['name'], cScheme)
                colorScheme = cScheme
                flash('Password Saved!', 'alert-success')
    return render_template('profile.html', logged = True, name = session['name'], title = "User Management", color = colorScheme)
@app.route('/webhook/add', methods=['POST', 'GET'])
@requires_login
def webh_add():
    colorScheme = dbManager.getColor(dbManager.getUserId(session['name']))[0][0]
    if request.method=='POST':
        name = request.form['name']
        avatar = request.form['avatar']
        url = request.form['url']
        service= request.form['service']
        owner = dbManager.getUserId(session['name'])
        dbManager.addWebhook(name,avatar,url,service,owner)
        return redirect('/profile/')
    return render_template('submitWebh.html', logged = True, name = session['name'], title = "New Webhook", webh = None, color = colorScheme)
@app.route('/webhook/edit/<webhId>', methods=['POST', 'GET'])
@requires_login
def webh_edit(webhId = None):
    colorScheme = dbManager.getColor(dbManager.getUserId(session['name']))[0][0]
    if request.method == 'POST':
        name = request.form['name']
        avatar = request.form['avatar']
        url = request.form['url']
        service= request.form['service']
        dbManager.editWebhook(webhId,name,avatar,url,service)
        return redirect('/profile/')
    else:
        if webhId == None:
            return redirect('/profile/')
        else:
            webh = dbManager.getWebhook(webhId)
            if webh == None:
                abort(404)
            else:
                if webh[0][5] != dbManager.getUserId(session['name']):
                    abort(403)
                else:
                    return render_template('submitWebh.html', logged = True, name = session['name'], title = "Edit Webhook", webh = webh, color = colorScheme)
@app.route('/logout')
def logout():
    session.pop('name', None)
    colorScheme = "red"
    return redirect('/')

app.secret_key = app.config['SECRET_KEY']
if __name__=="__main__":
    init(app)
    app.run(
        host = app.config['ip_address'],
        port = int(app.config['port']),
        debug = app.config['DEBUG']
    )
