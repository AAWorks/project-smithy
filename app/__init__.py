# Jimin: Alejandro Alonso (PM), Noakai Aronesty, Justin Zou, Ivan Lam
# SoftDev pd2
# P04 -- Smithy

from flask import Flask, render_template, request, session, redirect, url_for
from db_builder import *
from db_funcs import *

with open("db_builder.py", "rb") as source_file:
    code = compile(source_file.read(), "db_builder.py", "exec")
exec(code)

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

# authetication of login
@app.route("/auth", methods=['GET', 'POST'])
def authenticate():
    ''' Checks whether method is get, post. If get method, then redirect to
       loginpage. If post, then authenticate the username and password, rendering
       the error page if incorrect and the response.html if correct username/pass. '''

    # Variables
    method = request.method
    stuy_username = request.form.get('stuy_username').lower()
    password = request.form.get('password')

    # Get vs Post
    if method == 'GET':
        return redirect(url_for('disp_home'))

    auth_state = auth_user(stuy_username, password)
    if auth_state == "bad_pass":
        return render_template('login.html', input="bad_pass")
    elif auth_state == "bad_user":
        return render_template('login.html', input="bad_user")
    else:
        session['user_id'] = auth_state
        return redirect(url_for('disp_home'))


@app.route("/rAuth", methods=['GET', 'POST'])
def rAuthenticate():
    ''' Authentication of username and passwords given in register page from user '''

    method = request.method
    firstname = request.form.get('firstname').lower()
    lastname = request.form.get('lastname').lower()
    stuy_username = request.form.get('stuy_username').lower()
    password0 = request.form.get('password0')
    password1 = request.form.get('password1')

    if method == 'GET':
        return redirect(url_for('register'))

    if method == 'POST':
        # error when no username is inputted
        if len(stuy_username) == 0:
            return render_template('register.html', given="stuyvesant username")
        # error when no password is inputted
        elif len(password0) == 0:
            return render_template('register.html', given="password")
        elif len(password0) < 6:
            return render_template('register.html', given="password greater than 6 characters")
        # a username and password is inputted
        # a username and password is inputted
        else:
            # if the 2 passwords given don't match, will display error saying so
            if password0 != password1:
                return render_template('register.html', mismatch=True)
            else:
                # creates user account b/c no fails
                if create_user(stuy_username, password0, firstname, lastname):
                    return render_template('login.html', input='success')
                # does not create account because create_user failed (username is taken)
                else:
                    return render_template('register.html', taken=True)

@app.route("/logout")
def logout():
    ''' Logout user by deleting user from session dict. Redirects to loginpage '''
    # Delete user. This try... except... block prevent an error from ocurring when the logout page is accessed from the login page
    try:
        session.pop('user_id')
    except KeyError:
        return redirect(url_for('disp_home'))
    # Redirect to login page
    return redirect(url_for('disp_home'))

@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def disp_home():
    ''' Loads the landing page '''
    try:
        return render_template("home.html")
    except:
        return render_template("error.html")

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()