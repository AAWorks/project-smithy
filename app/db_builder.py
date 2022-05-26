import sqlite3
from flask import session

DB_FILE = "discobandit.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

def create_db():
    ''' Creates / Connects to DB File '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS Login (usernames TEXT, passwords TEXT, classRanking INTEGER);")
    c.execute("CREATE TABLE IF NOT EXISTS Projects (Project_ID INTEGER, Project_Title TEXT, Authors TEXT, Avg_Rating INTEGER);")


    db.close()