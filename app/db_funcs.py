# Jimin: Alejandro Alonso (PM), Noakai Aronesty, Justin Zou, Ivan Lam
# SoftDev pd2
# P04 -- Smithy

""" Supplemental functions """

import sqlite3, hashlib, bcrypt, datetime
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
    year = datetime.date.today().year if datetime.date.today().month < 7 else datetime.date.today().year + 1

    rowid = db.insert("users", pfp=pfp, stuy_username=stuy_username, password=hashsalt(password), firstname=firstname, lastname=lastname, github=github, devostatus=devo_status, year=year)
    db.insert('user_details', rowid)
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
    '''updates a user's account data'''
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
    return list(set(project_ids))

def get_details(user_id):
    db = SqliteDb(DB_FILE)
    return db.select("user_details", user_id=user_id)[0]

def get_full_username(user_id):
    db = SqliteDb(DB_FILE)
    return db.select("users", user_id=user_id)[0].stuy_username + "#" + str(user_id)

def edit_user_details(user_id, about, back_end, front_end, git_foo, can_serve, discord_name, discord_id, facebook_name, twitter_name, reddit_name):
    '''updates a user's account details'''
    db = SqliteDb(DB_FILE)
    db.update("user_details", where={"user_id": user_id}, about=about, back_end=back_end, front_end=front_end, git_foo=git_foo, can_serve=can_serve, discord_name=discord_name, discord_id=discord_id, facebook_name=facebook_name, twitter_name=twitter_name, reddit_name=reddit_name)

def delete_user(user_id):
    db = SqliteDb(DB_FILE)
    db.delete("users", user_id=user_id)

def clear_users_table():
    check = input("YOU ARE ABOUT TO DELETE EVERY ENTRY IN THE USERS TABLE OF THE DATABASE. CONTINUE (Y/N): ")
    if check != "Y":
        return False
    db = SqliteDb(DB_FILE)
    db.delete_all("users")

def edit_user_name(user_id, first, last):
    db = SqliteDb(DB_FILE)
    db.update("users", where={"user_id": user_id}, firstname=first, lastname=last)

def get_comment(comment_id):
    '''get a comment by id'''
    db = SqliteDb(DB_FILE)
    return db.select("comment", comment_id=comment_id)[0]

def insert_comment(comment, user_id, user_pfp, user_name, project_id, anonymous):
    '''insert a comment into the comments table'''
    db = SqliteDb(DB_FILE)
    anonymous_thing = 0
    #print(anonymous == "on")
    if (anonymous):
        anonymous_thing=1
    #print(anonymous_thing)
    db.insert("comments", comment=comment, user_id=user_id, user_pfp=user_pfp, user_name=user_name, project_id=project_id, anonymous=anonymous_thing)

def del_comment(comment_id):
    db = SqliteDb(DB_FILE)
    db.delete("comments", comment_id=comment_id)

def upvote_comment(comment_id, user_id):
    '''upvote a comment from a user'''
    db = SqliteDb(DB_FILE)
    db.upsert("votes", where={"comment_id": comment_id, "user_id": user_id}, vote=1)

def downvote_comment(comment_id, user_id):
    '''downvote a comment from a user'''
    db = SqliteDb(DB_FILE)
    db.upsert("votes", where={"comment_id": comment_id, "user_id": user_id}, vote=-1)

def neutralize_comment(comment_id, user_id):
    '''downvote a comment from a user'''
    db = SqliteDb(DB_FILE)
    db.upsert("votes", where={"comment_id": comment_id, "user_id": user_id}, vote=0)

def get_comment_rating(comment_id):
    '''return a comment's overall rating from up and downvotes'''
    db = SqliteDb(DB_FILE)
    votes = db.select('votes', comment_id=comment_id)
    ret = 0
    for vote in votes:
        ret += vote['vote']
    return ret

def get_user_votes(user_id):
    db = SqliteDb(DB_FILE)
    return db.select('votes', user_id=user_id)

def get_devos_by_class(years):
    db = SqliteDb(DB_FILE)
    user_classes = {k:[] for k in years}

    for year in years:
        user_classes[year] = db.select("users", year=int(year))

    return user_classes
