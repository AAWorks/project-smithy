from notanorm import SqliteDb
import itertools
from db_funcs import *
import db_builder

newstr = "(40 − 70)2 × 0.4 + (60 − 70)2 × 0.05 + (68 − 70)2 × 0.04 + (70 − 70)2 × 0.02 + (72 − 70)2 × 0.04 + (80 − 70)2 × 0.05 + (100 − 70)2 × 0.4"
print(newstr.replace("×", "*").replace("2", "^2"))


"""
db = SqliteDb("project_reviewal.db")
print(db.select("users"))
"""

"""
if False:
    path = "var/www/app/"
else:
    path= ""

DB_FILE = path + "project_reviewal.db"

common_firsts = ["liam", "noah", "oliver", "elijah", "james", "william", "benjamin", "lucas", "henry", "theodore"]
common_lasts = ["smith", "johnson", "williams", "brown", "jones", "miller", "davis", "garcia", "rodriguez", "wilson"]
combined = [x for x in itertools.chain.from_iterable(itertools.zip_longest(common_firsts,common_lasts)) if x]

stuyusers = [(combined[i][0] + combined[i+1] + "20") for i in range(0, len(combined), 2)]

for i in range(10):
    create_user(stuyusers[i], "password", common_firsts[i], common_lasts[i], stuyusers[i], "static/images/users/default.png", "Student")
"""