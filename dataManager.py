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

def checkPassword(input, hashedPw):
    return hashedPw == bcrypt.hashpw(input.encode('utf-8'), hashedPw.encode('utf-8'))
