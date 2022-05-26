# PPP Mode: Ivan Mijacika, Qina Liu, Justin Morrill, Noakai Aronesty
# SoftDev pd2
# P02 -- Snake++

""" Authentication / Creation of Users """

import sqlite3
from notanorm import SqliteDb

DB_FILE = "project_reviewal.db"

def create_db():
    ''' Creates / Connects to DB File '''

    db = SqliteDb(DB_FILE)
    db.query("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, stuy_username TEXT, password TEXT, firstname TEXT, lastname TEXT);")
    db.query("CREATE TABLE IF NOT EXISTS projects (project_id INTEGER PRIMARY KEY AUTOINCREMENT, project_title TEXT, author_ids TEXT, rating INTEGER);")
    db.query("CREATE TABLE IF NOT EXISTS comments (comment TEXT, project_id INTEGER, upvotes INTEGER, downvotes INTEGER, anonymous INTEGER);")
    db.query("CREATE TABLE IF NOT EXISTS ratings (project_id INTEGER, user_id INTEGER, rating INTEGER);")
    db.query("CREATE TABLE IF NOT EXISTS favorites (user_id INTEGER, project_id INTEGER);")

    db.close()


def auth_user(stuy_username, password):
    ''' Validates a username + password when person logs in '''

    db = SqliteDb(DB_FILE)

    # Create List of Users
    stuy_usernames = [u.stuy_username for u in db.select("users")]
    if stuy_username not in stuy_usernames:
        return "bad_user"

    
    possible_users = db.select("users", stuy_username=stuy_username)
    for i in possible_users:
        if i.password == password:
            return i.user_id
    return "bad_pass"


def create_user(stuy_username, password, firstname, lastname):
    ''' Adds user to database if right username and password are given when a
        person registers '''

    db = SqliteDb(DB_FILE)

    # Create List of Users
    passwords = [u.password for u in db.select("users", stuy_username=stuy_username)]
    print(passwords)

    # password is not taken, creates account with given username and password

    if password in passwords:
        return False
    else:
        db.insert("users", stuy_username=stuy_username, password=password, firstname=firstname, lastname=lastname)
        return True


create_db()

# For testing purposes #################

# db = sqlite3.connect(DB_FILE)
# c = db.cursor()
# c.execute("SELECT usernames FROM users")
# users = []
# for a_tuple in c.fetchall():
#     users.append(a_tuple[0])
# print(users)