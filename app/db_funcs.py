# Jimin: Alejandro Alonso (PM), Noakai Aronesty, Justin Zou, Ivan Lam
# SoftDev pd2
# P04 -- Project Reviewal System

""" Supplemental functions """

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