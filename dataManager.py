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
    print(id[0][0])
    return id[0][0]

def checkPassword(input, hashedPw):
    return hashedPw == bcrypt.hashpw(input.encode('utf-8'), hashedPw.encode('utf-8'))

def addWebHook(name,avatar,url,owner):
    conn = sql.connect(dbLocation)
    cur = conn.cursor()
    cur.execute("INSERT INTO webhook (name,avatar,url,owner) VALUES (?,?,?,?)", (name,avatar,url,owner))
    conn.commit()
    conn.close()
