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


def create_user(stuy_username, password, firstname, lastname, github, pfp):
    ''' Adds user to database if right username and password are given when a
        person registers '''

    db = SqliteDb(DB_FILE)
    devo_status = "Devo-In-Training"
    db.insert("users", pfp=pfp, stuy_username=stuy_username, password=hashsalt(password), firstname=firstname, lastname=lastname, github=github, devostatus=devo_status)
    db.insert('user_details', about="", back_end=0, front_end=0, can_serve=0)
    return True

def get_latest_id(stuy_username):
    '''returns the latest user_id in the table for a stuy_username'''
    db = SqliteDb(DB_FILE)
    ret = db.select("users", stuy_username=stuy_username)[-1].user_id
    return ret

def get_user(user_id):
    '''returns user row based on user_id'''
    db = SqliteDb(DB_FILE)

    return db.select("users", user_id=user_id)[0]

def edit_user_data(table, user_id, column_toEdit, new_val):
    '''updates a user's account details'''
    db = SqliteDb(DB_FILE)

    db.update(table, where={"user_id": user_id}, upd={column_toEdit: new_val})

def get_users():
    '''fetches all users'''
    db = SqliteDb(DB_FILE)
    return db.select("users")

def get_project_ids(user_id):
    '''gets a user's project IDs'''
    db = SqliteDb(DB_FILE)
    project_ids = [u.project_id for u in db.select("projects", pmID=user_id)]
    for i in db.select("projects"):
        if str(user_id) in i.devoIDs.split("|"):
            project_ids.append(i.project_id)
    return project_ids

def get_details(user_id):
    db = SqliteDb(DB_FILE)
    return db.select("user_details", user_id=user_id)[0]

def get_full_username(user_id):
    db = SqliteDb(DB_FILE)
    return db.select("users", user_id=user_id)[0].stuy_username + "#" + str(user_id)