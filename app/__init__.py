from flask import Flask, render_template, request, session, redirect, url_for

with open("app/db_builder.py", "rb") as source_file:
    code = compile(source_file.read(), "app/db_builder.py", "exec")
exec(code)

with open("app/auth.py", "rb") as source_file:
    code2 = compile(source_file.read(), "app/auth.py", "exec")
exec(code2)

app = Flask(__name__)
app.secret_key = 'stuffins'

@app.route('/login', methods=['GET','POST'])
def login():
    try:
        return render_template("login.html")
    except:
        return render_template("error.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        return render_template("register.html")
    except:
        return render_template("error.html")

@app.route('/terms', methods=['GET', 'POST'])
def terms():
    terms = open("static/terms.txt", encoding="utf8")
    terms_lines = terms.readlines()
    terms.close()
    try:
        return render_template("terms.html", terms=terms_lines)
    except:
        return render_template("error.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    try:
        return render_template("home.html")
    except:
        return render_template("error.html")

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()