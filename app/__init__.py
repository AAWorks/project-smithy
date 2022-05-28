# Jimin: Alejandro Alonso (PM), Noakai Aronesty, Justin Zou, Ivan Lam
# SoftDev pd2
# P04 -- Smithy

from flask import Flask, render_template, request, session, redirect, url_for
from db_builder import *
from db_funcs import *

"""
with open("app/db_builder.py", "rb") as source_file:
    code = compile(source_file.read(), "app/db_builder.py", "exec")
exec(code)
with open("app/db_funcs.py", "rb") as source_file:
    code = compile(source_file.read(), "app/db_funcs.py", "exec")
exec(code)
"""

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
    with app.open_resource('static/terms.txt') as terms:
        terms_lines = [line.decode("utf8") for line in terms.readlines()]
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
    user_id = request.form.get('user_id')
    password = request.form.get('password')

    try:
        stuy_username = request.form.get('stuy_username').lower()
        user_id = request.form.get('user_id')
    except:
        return render_template('login.html', input="bad_user")
    
    try:
        password = request.form.get('password')
    except:
        return render_template('login.html', input="bad_pass")

    # Get vs Post
    if method == 'GET':
        return redirect(url_for('disp_home'))

    try:
        auth_state = auth_user(stuy_username, user_id, password)
    except:
        return render_template('login.html', input="bad_user")
    
    if auth_state == "bad_pass":
        return render_template('login.html', input="bad_pass")
    elif auth_state == "bad_user":
        return render_template('login.html', input="bad_user")
    elif auth_state == True:
        session['user_id'] = stuy_username + "#" + str(user_id)
        return redirect('account')


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
                create_user(stuy_username, password0, firstname, lastname)
                return render_template('login.html', input='success', user_id=get_latest_id(stuy_username))

@app.route("/edit")
def editProfile():
    try:
        if session:
            user = get_user(int(session['user_id'].split('#')[-1]))
            name = user["firstname"] + " " + user["lastname"]
            return render_template("edit.html", first=user["firstname"].title(), name=name.title(), user_id=session['user_id'], stuyname=user["stuy_username"])
        else:
            return render_template("home.html")
    except:
        return render_template("error.html")

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
        if session:
            return render_template("home.html", returning="Current user: " + session['user_id'])
        else:
            return render_template("home.html")
    except:
        return render_template("error.html")

@app.route("/account", methods=['GET', 'POST'])
def account():
    try:
        if session:
            user = get_user(int(session['user_id'].split('#')[-1]))
            name = user["firstname"] + " " + user["lastname"]
            return render_template("account.html", first=user["firstname"].title(), name=name.title(), user_id=session['user_id'], stuyname=user["stuy_username"])
        else:
            return redirect("/login")
    except:
        return render_template("error.html")

@app.route("/about", methods=['GET', 'POST'])
def about():
    try:
        return render_template("about.html")
    except:
        return render_template("error.html")

@app.route("/devos", methods=['GET', 'POST'])
def devos():
    try:
        tester = {"name": "Thluffy Sinclair", "id": "tsinclair20", "bio": "A totally tubular devo to test the totally tubular devos page!", "pfp": url_for('static', filename="images/default_pfp.png")}
        devos=[]
        for i in range(10):
            devo = {}
            devo["name"] = tester['name']
            devo["id"] = tester['id'] + "#" + str(i)
            devo["bio"] = tester["bio"]
            devo["pfp"] = tester["pfp"]
            devos.append(devo)
        return render_template("devos.html", devos=devos)
    except:
        return render_template("error.html")

@app.route("/gallery", methods=['GET', 'POST'])
def gallery():
    try:
        tester = {"title": "Tester", "descrip": "A totally tubular project to test the totally tubular gallery!", "image": url_for('static', filename="images/Smithy.png")}
        projects=[]
        for i in range(10):
            tmp = {}
            tmp["title"] = tester['title'] + str(i)
            tmp["descrip"] = tester['descrip']
            tmp["image"] = tester["image"]
            projects.append(tmp)
        return render_template("gallery.html", projects=projects)
    except:
        return render_template("error.html")
    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()