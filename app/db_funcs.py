# Jimin: Alejandro Alonso (PM), Noakai Aronesty, Justin Zou, Ivan Lam
# SoftDev pd2
# P04 -- Smithy

""" Supplemental functions """

import sqlite3, hashlib, bcrypt
from notanorm import SqliteDb

DB_FILE = "project_reviewal.db"

def hashsalt(password: str):
    pwd = bytes(password, 'utf-8')

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd, salt)

    return hashed

def check_pw(password: str, stored_pw):
    pwd = bytes(password, 'utf-8')
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd, salt)

    match = bcrypt.checkpw(stored_pw, hashed)
    return match

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

    if check_pw(password, db.select("users", user_id=user_id)[0].password):
        return "bad_pass"

    return True


def create_user(stuy_username, password, firstname, lastname, github):
    ''' Adds user to database if right username and password are given when a
        person registers '''

    db = SqliteDb(DB_FILE)
    devo_status = "Devo-In-Training"
    db.insert("users", stuy_username=stuy_username, password=hashsalt(password), firstname=firstname, lastname=lastname, github=github, devostatus=devo_status)
    return True

def get_latest_id(stuy_username):
    db = SqliteDb(DB_FILE)
    ret = db.select("users", stuy_username=stuy_username)[-1].user_id
    return ret

def get_user(user_id):
    '''returns user row based on user_id'''
    db = SqliteDb(DB_FILE)

    return db.select("users", user_id=user_id)[0]