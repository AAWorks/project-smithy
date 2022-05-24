from flask import Flask, render_template, request, session, redirect, url_for

with open("app/db_builder.py", "rb") as source_file:
    code = compile(source_file.read(), "app/db_builder.py", "exec")
exec(code)

app = Flask(__name__)
app.secret_key = 'physiscmakesmesad'

@app.route('/', methods=['GET','POST'])
def login():
    try:
        return render_template("login.html")
    except:
        return render_template("error.html")

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()