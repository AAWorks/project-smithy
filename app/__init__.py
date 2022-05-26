from flask import Flask, render_template, request, session, redirect, url_for

with open("db_builder.py", "rb") as source_file:
    code = compile(source_file.read(), "db_builder.py", "exec")
exec(code)

app = Flask(__name__)
app.secret_key = 'physiscmakesmesad'

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

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()