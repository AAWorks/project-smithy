from notanorm import SqliteDb
import itertools
from db_funcs import *

DB_FILE = "project_reviewal.db"

db=SqliteDb(DB_FILE)

db.delete_all("projects")