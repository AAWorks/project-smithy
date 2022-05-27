# Jimin: Alejandro Alonso (PM), Noakai Aronesty, Justin Zou, Ivan Lam
# SoftDev pd2
# P04 -- Smithy

""" Supplemental functions """

import sqlite3
from notanorm import SqliteDb

DB_FILE = "project_reviewal.db"

def auth_user(stuy_username, user_id, password):
    ''' Validates a username + password when person logs in '''

    db = SqliteDb(DB_FILE)

    # Create List of Users
    user_ids = [u.user_id for u in db.select("users", stuy_username=stuy_username)]
    
    # testing
    # print("user id: " + user_id)
    # print(user_ids)
    # print(int(user_id) in user_ids)
    if int(user_id) not in user_ids:
        return "bad_user"

    if password != db.select("users", user_id=user_id)[0].password:
        return "bad_pass"

    return True


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