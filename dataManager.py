import sqlite3 as sql
import bcrypt
dbLocation = "var/data.db"


def signUp(username,password):
    conn = sql.connect(dbLocation)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
    conn.commit()
    conn.close()

def retrieveUsers():
	conn = sql.connect(dbLocation)
	cur = conn.cursor()
	cur.execute("SELECT username, password FROM users")
	users = cur.fetchall()
	conn.close()
	return users

def checkLogIn(username, password):
    result = False
    users = retrieveUsers()
    for user in users:
        dbUsrName=user[0]
        dbPass=user[1]
        if dbUsrName == username:
            result = checkPassword(password, dbPass)
    return result

def checkUserExists(username):
    result = False
    conn = sql.connect(dbLocation)
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM users WHERE username = ?",(username,))
    count = cur.fetchall()
    print (count[0][0])
    conn.close()
    if count[0][0] == 1:
        result = True
    return result
def getUserId(username):
    conn = sql.connect(dbLocation)
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?",(username,))
    id = cur.fetchall()
    conn.close()
    return id[0][0]
def checkPassword(input, hashedPw):
    return hashedPw == bcrypt.hashpw(input.encode('utf-8'), hashedPw.encode('utf-8'))
def editPassword(username, newPassword):
    conn = sql.connect(dbLocation)
    cur = conn.cursor()
    cur.execute("UPDATE users SET password = ? WHERE username = ?",(newPassword,username))
    conn.commit()
    conn.close()

def addWebhook(name,avatar,url,service, owner):
    conn = sql.connect(dbLocation)
    cur = conn.cursor()
    cur.execute("INSERT INTO webhook (name,avatar,url,service,owner) VALUES (?,?,?,?,?)", (name,avatar,url,service,owner))
    conn.commit()
    conn.close()
def getWebhookList(userid):
    conn = sql.connect(dbLocation)
    cur = conn.cursor()
    cur.execute("SELECT name, service, avatar, url, id FROM webhook WHERE owner = ?",(int(userid),))
    webhooks = cur.fetchall()
    conn.close()
    return webhooks
def getWebhook(webhId):
    conn = sql.connect(dbLocation)
    cur = conn.cursor()
    cur.execute("SELECT name, service, avatar, url, id, owner FROM webhook WHERE id = ?",(int(webhId),))
    webhook = cur.fetchall()
    conn.close()
    return webhook
def deleteWebhook(id):
    conn = sql.connect(dbLocation)
    cur = conn.cursor()
    cur.execute("DELETE FROM webhook WHERE id = ?",(id,))
    conn.commit()
    conn.close()
def editWebhook(id,name,avatar,url,service):
    conn = sql.connect(dbLocation)
    cur = conn.cursor()
    cur.execute("UPDATE webhook SET name = ?, avatar = ?, url = ?, service = ? WHERE id = ?",(name,avatar,url,service,id))
    conn.commit()
    conn.close()
