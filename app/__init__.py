# Jimin: Alejandro Alonso (PM), Noakai Aronesty, Justin Zou, Ivan Lam
# SoftDev pd2
# P04 -- Smithy

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_cors import CORS
from werkzeug import *
from hashlib import md5
import os
import datetime
from datetime import date
import re

with open("app/db_builder.py", "rb") as source_file:
    code = compile(source_file.read(), "app/db_builder.py", "exec")
exec(code)
with open("app/db_funcs.py", "rb") as source_file:
    code = compile(source_file.read(), "app/db_funcs.py", "exec")
exec(code)
with open("app/project_db.py", "rb") as source_file:
    code = compile(source_file.read(), "app/project_db.py", "exec")
exec(code)

PROJECTS_UPLOAD_FOLDER = 'app/static/images/projects'
USERS_UPLOAD_FOLDER = 'app/static/images/users'
ALLOWED_EXTENSIONS = {'png'}

app = Flask(__name__)
cors = CORS(app)
app.secret_key = 'stuffins'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def avatar(size, email):
    digest = md5(email.lower().encode('utf-8')).hexdigest()
    return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}' + '.jpg'


@app.route('/login', methods=['GET', 'POST'])
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

    try:
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
            session['user_id'] = user_id
            return redirect(url_for('user_account', user_id=user_id))
    except:
        return render_template("error.html")


@app.route("/rAuth", methods=['GET', 'POST'])
def rAuthenticate():
    ''' Authentication of username and passwords given in register page from user '''
    try:
        method = request.method
        firstname = request.form.get('firstname').title()
        lastname = request.form.get('lastname').title()
        stuy_username = request.form.get('stuy_username').lower()
        github = request.form.get('github')
        password0 = request.form.get('password0')
        password1 = request.form.get('password1')

        if method == 'GET':
            return redirect(url_for('register'))

        if method == 'POST':
            # error when no username is inputted
            if len(github) == 0:
                return render_template('register.html', given="github username")
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
                    create_user(stuy_username, password0,
                                firstname, lastname, github, url_for('static', filename='images/users/default.png'))
                    return render_template('login.html', input='success', user_id=get_latest_id(stuy_username))
    except:
        return render_template("error.html")


@app.route("/edit")
def editProfile():
    try:
        if not session:
            return redirect('/login')
        user = get_user(session['user_id'])
        details = get_details(session['user_id'])
        about_info = []
        about_last = ""
        if (details['about']):
            for i in details['about'].split('\r\n'):
                about_info.append(i)
            about_last = about_info[-1]
        return render_template("edit.html",
                               average_given_rating=get_average_rating_given(
                                   user['user_id']),
                               pfp=avatar(
                                   315, user['stuy_username'] + "@stuy.edu"),
                               first=user["firstname"].title(),
                               last=user['lastname'].title(),
                               user_id=session['user_id'],
                               stuyname=user["stuy_username"],
                               github=user["github"],
                               devo_status=user["devostatus"],
                               about_info=about_info[:-1],
                               about_last=about_last,
                               back_end_info=details['back_end'],
                               front_end_info=details['front_end'],
                               git_foo_info=details['git_foo'],
                               can_serve_info=details['can_serve'],
                               discord_name=details['discord_name'],
                               discord_id=details['discord_id'],
                               facebook_name=details['facebook_name'],
                               twitter_name=details['twitter_name'],
                               reddit_name=details['reddit_name'])
    except:
        return render_template("error.html")


@app.route('/update_info', methods=['GET', 'POST'])
def update_info():
    try:
        if not session:
            return redirect('/login')
        method = request.method
        about_info = request.form.get('about_section')
        user_id = request.form.get('user_id')
        back_end_info = int(request.form.get('back_end_range'))
        front_end_info = int(request.form.get('front_end_range'))
        git_foo_info = int(request.form.get('git_foo_range'))
        can_serve_info = request.form.get('can_serve_select')
        discord_name = request.form.get('discord_name')
        discord_id = request.form.get('discord_id')
        facebook_name = request.form.get('facebook_name')
        twitter_name = request.form.get('twitter_name')
        reddit_name = request.form.get('reddit_name')
        first = request.form.get('first').lower()
        last = request.form.get('last').lower()
        if first == "":
            edit_user_details(user_id, about_info, back_end_info, front_end_info, git_foo_info, can_serve_info,
                              discord_name, discord_id, facebook_name, twitter_name, reddit_name)
            return redirect(url_for('user_account', user_id=user_id))

        if method == 'GET':
            return redirect(url_for('disp_home'))

        if method == 'POST':
            if (discord_name and not discord_id) or (not discord_name and discord_id):
                return redirect(url_for('editProfile', discord_not_match='true'))
            else:
                edit_user_details(user_id, about_info, back_end_info, front_end_info, git_foo_info, can_serve_info,
                                  discord_name, discord_id, facebook_name, twitter_name, reddit_name)
                edit_user_name(user_id, first, last)
                return redirect(url_for('user_account', user_id=user_id))
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
    if session:
        if(date.today() == date(2022, 6, 14)):
            updateDevosStatus()
        return render_template("home.html", returning="Current user: " + get_full_username(session['user_id']))
        
        # session['user_id']
    else:
        return render_template("home.html")
   


@app.route("/account/<user_id>", methods=['GET', 'POST'])
def user_account(user_id):
    # try:
    user = get_user(user_id)
    details = get_details(user_id)
    name = user["firstname"] + " " + user["lastname"]
    project_ids = get_project_ids(user.stuy_username + "#" + str(user_id))
    project_snaps = [get_project_snapshot(
        project_id) for project_id in project_ids]

    about_info = []
    if (details['about']):
        for i in details['about'].split('\r\n'):
            about_info.append(i)

    if session:
        user_match = (int(session['user_id']) == int(user['user_id']))
    else:
        user_match = False

    project_snaps.reverse()
    return render_template("account.html",
                           average_given_rating=get_average_rating_given(
                               user['user_id']),
                           user_id=user['user_id'],
                           pfp=avatar(
                               315, user['stuy_username'] + "@stuy.edu"),
                           first=user["firstname"].title(),
                           name=name.title(),
                           stuyname=user["stuy_username"],
                           github=user["github"],
                           devo_status=user["devostatus"],
                           about_info=about_info,
                           back_end_info=details['back_end'],
                           front_end_info=details['front_end'],
                           git_foo_info=details['git_foo'],
                           can_serve_info=details['can_serve'],
                           discord_name=details['discord_name'],
                           discord_id=details['discord_id'],
                           facebook_name=details['facebook_name'],
                           twitter_name=details['twitter_name'],
                           reddit_name=details['reddit_name'],
                           user_match=user_match,
                           num_projs=len(get_project_ids(
                               user.stuy_username + "#" + str(user.user_id))),
                           projects=project_snaps
                           )
    # except:
 #   return render_template("error.html")


@app.route("/devos", methods=['GET', 'POST'])
def devos():
    # try:
    # tester = {"name": "Thluffy Sinclair", "id": "tsinclair20", "bio": "A totally tubular devo to test the totally tubular devos page!",
    #           "pfp": url_for('static', filename="images/users/default.png")}
    # devos = []
    # for i in range(10):
    #     devo = {}
    #     devo["name"] = tester['name']
    #     devo["id"] = tester['id'] + "#" + str(i)
    #     devo["bio"] = tester["bio"]
    #     devo["pfp"] = tester["pfp"]
    #     devos.append(devo)
    # try:

    # if devos() is receiving info, set users to users sorted by class
    curr_grad_year = datetime.date.today().year if datetime.date.today(
    ).month < 7 else datetime.date.today().year + 1
    users = get_devos_by_class([str(year)
                               for year in range(2022, curr_grad_year + 1)])

    for year in users.keys():
        for i in range(len(users[year])):
            u = users[year][i]
            users[year][i] = {
                "name": (u.firstname + " " + u.lastname).title(),
                "user_id": u.user_id,
                "stuyname": u.stuy_username,
                "num_projs": len(get_project_ids(u.stuy_username + "#" + str(u.user_id))),
                "bio": get_details(u.user_id)["about"],
                "pfp": avatar(300, u.stuy_username + "@stuy.edu")
            }

    # Display more recent devos first, so devos from previous years aren't at the top
    # devos.reverse()

    return render_template("devos.html", devos=users)
    # except:
 #   return render_template("error.html")


@app.route("/gallery", methods=['GET', 'POST'])
def gallery():
    try:
        project_ids = get_all_project_ids()
        project_snaps = []

        if request.method == 'POST' and request.form.get('sort') == 'rating':
            project_snaps = get_projects_by_star_rating()
        else:
            for project_id in project_ids:
                project_snaps.append(get_project_snapshot(project_id))

        # Display more recent projects first, so projects from previous years aren't at the top
        project_snaps.reverse()

        return render_template("gallery.html", projects=project_snaps)
    except:
        return render_template("error.html")


@app.route("/project/<project_id>/<comment_empty>", methods=['GET', 'POST'])
def view_project(project_id, comment_empty):
    # try:
    project = get_project_details(project_id)

    pm_id = project['pmID'].split("#")[-1]
    pm = get_user(pm_id)
    pm_name = (pm['firstname'] + " " + pm['lastname']).title()
    comments = get_project_comments(project_id)

    for comment in comments:
        comment['rating'] = get_comment_rating(comment['comment_id'])
        comment['vote']=0
        if session:
            for vote in get_user_votes(session['user_id']):
                if int(vote['comment_id']) == int(comment['comment_id']):
                    comment['vote']=vote['vote']
                    break
                # print(comment['vote'])


    devos = []
    for full_devo_id in project['devoIDs']:
        if full_devo_id != "":
            devo_id = full_devo_id.split("#")[-1]
            devo_info = get_user(devo_id)
            devo = {'name': (
                devo_info['firstname'] + " " + devo_info['lastname']).title(), 'id': devo_id}
            devos.append(devo)

    if project['hosted_loc'].startswith("http://") or project['hosted_loc'].startswith("https://"):
        hosted = True
    else:
        hosted = False

    if session:
        star5 = request.form.get('star5')
        star4half = request.form.get('star4half')
        star4 = request.form.get('star4')
        star3half = request.form.get('star3half')
        star3 = request.form.get('star3')
        star2half = request.form.get('star2half')
        star2 = request.form.get('star2')
        star1half = request.form.get('star1half')
        star1 = request.form.get('star1')
        starhalf = request.form.get('starhalf')
        if request.method == 'POST':
            if(star5):
                updateRating(project_id, star5, session['user_id'])
            elif(star4half):
                updateRating(project_id, star4half, session['user_id'])
            elif(star4):
                updateRating(project_id, star4, session['user_id'])
            elif(star3half):
                updateRating(project_id, star3half, session['user_id'])
            elif(star3):
                updateRating(project_id, star3, session['user_id'])
            elif(star2half):
                updateRating(project_id, star2half, session['user_id'])
            elif(star2):
                updateRating(project_id, star2, session['user_id'])
            elif(star1half):
                updateRating(project_id, star1half, session['user_id'])
            elif(star1):
                updateRating(project_id, star1, session['user_id'])
            elif(starhalf):
                updateRating(project_id, starhalf, session['user_id'])
            return render_template("project.html", starratings=getAvgRating(project_id), project_id=project_id, title=project['title'], project_image=project['image'], team_name=project['team_name'], tags=project['tags'], project_descrip_1=project['intro'], project_descrip_2=project['descrip'], pm_id=pm_id, pm_name=pm_name, devos=devos, repo_link=project['repo'], hosted=hosted, hosted_loc=project['hosted_loc'], team_flag=project['team_flag'], comments=comments, comment_empty=comment_empty)

    return render_template("project.html",
                           starratings=getAvgRating(project_id),
                           project_id=project_id, 
                           title=project['title'], 
                           project_image=project['image'], 
                           team_name=project['team_name'], 
                           tags=project['tags'], 
                           project_descrip_1=project['intro'], 
                           project_descrip_2=project['descrip'], 
                           pm_id=pm_id, 
                           pm_name=pm_name, 
                           devos=devos, 
                           repo_link=project['repo'], 
                           hosted=hosted, 
                           hosted_loc=project['hosted_loc'], 
                           team_flag=project['team_flag'], 
                           comments=comments, 
                           comment_empty=comment_empty
                           )
    # except:
 #  return render_template("error.html")


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    try:
        if not session:
            return redirect('/login')
        user = get_user(session['user_id'])
        error = ""

        if request.method == 'POST':
            # error handling
            if len([field for field in request.form if field != ""]) == 0:
                return render_template("upload_project.html", user_id=user, error="Missing inputs - like, all of them.")
            for field in request.form:
                if not request.form.get(field) and field != 'hosted_loc' and not field.startswith('devo'):
                    fieldname = field if field != 'descrip' else "'Why this project?'"
                    return render_template("upload_project.html", user_id=user, error="Missing input - " + fieldname.title() + ".")
                elif field in ['hosted_loc', 'repo'] and request.form.get(field) and not request.form.get(field).startswith('http://') and not request.form.get(field).startswith('https://'):
                    return render_template("upload_project.html", user_id=user, error="Falty input - website links should start with 'http://'")
                elif field in ['title', 'team_name', 'summary', 'descrip'] and len([x for x in request.form.get(field).split(" ") if len(x) >= 35]) != 0:
                    return render_template("upload_project.html", user_id=user, error="Falty input - Words must be less than 40 characters.")

            # end error handling

            app.config['UPLOAD_FOLDER'] = PROJECTS_UPLOAD_FOLDER
            cover_photo = request.files['project_image']
            flag = request.files['team_flag']
            devoIDs = []
            tmpdevs = [x for x in [request.form.get('devo1'), request.form.get(
                'devo2'), request.form.get('devo3')] if x != ""]
            for i in range(0, len(tmpdevs)):
                dev = request.form.get('devo' + str(i+1))
                try:
                    dev_id = dev.split("#")[-1]
                    get_user(dev_id)
                except:
                    return render_template("upload_project.html", user_id=user, error="Devo IDs must match to ACTUAL devos.")
                if dev:
                    devoIDs.append(dev)
            tags = ["Project " + request.form.get('project_num')]

            pm_id = request.form.get('pm_id').split("#")[-1]
            try:
                get_user(pm_id)
                if int(session['user_id']) != int(pm_id):
                    return render_template("upload_project.html", user_id=user, error="You must be the PM to upload a project.")
            except:
                return render_template("upload_project.html", user_id=user, error="PM ID must math to an ACTUAL devo.")

            if cover_photo.filename != "" and allowed_file(cover_photo.filename) and flag.filename != "" and allowed_file(flag.filename):
                new_project = upload_project(request.form.get('title'), url_for('static', filename='images/projects/default.png'), request.form.get('team_name'), request.form.get(
                    'pm_id'), devoIDs, tags, request.form.get('repo'), request.form.get('summary'), request.form.get('descrip'), 0, request.form.get('hosted_loc'), url_for('static', filename='images/projects/default.png'))
                pid = new_project['project_id']
                cover_filename = str(pid) + "_cover" + ".png"
                cover_photo.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], cover_filename))
                edit_project_info(pid, 'image', url_for(
                    'static', filename='images/projects/' + cover_filename))
                flag_filename = str(pid) + "_flag" + ".png"
                flag.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], flag_filename))
                edit_project_info(pid, 'team_flag', url_for(
                    'static', filename='images/projects/' + flag_filename))
                return redirect(url_for('view_project', project_id=pid, comment_empty=0))
            else:
                return render_template("upload_project.html", user_id=user, error="Submit PNG files (smaller than 500KB) for your cover and team flag photos.")

        return render_template("upload_project.html", user_id=user, error=error)
    except:
        return render_template("error.html")


@app.route("/post_comment", methods=['GET', 'POST'])
def post_comment():
    try:
        if not session:
            return redirect('/login')
        method = request.method
        comment = request.form.get('comment')
        anonymous = request.form.get('anonymous')
        user = get_user(session['user_id'])
        project_id = int(request.form.get('project_id'))

        if method == 'GET':
            return redirect(url_for('disp_home'))

        if method == 'POST':
            if comment == "":
                return redirect(url_for('view_project', project_id=project_id, comment_empty=1) + "#comments_section")
            else:
                insert_comment(comment, user.user_id, avatar(128, user.stuy_username +
                               "@stuy.edu"), user.firstname + " " + user.lastname, project_id, anonymous)
                return redirect(url_for('view_project', project_id=project_id, comment_empty=0))
    except:
        return render_template("error.html")


@app.route("/delete_comment", methods=['GET', 'POST'])
def delete_comment():
    # try:
    if not session:
        return redirect('/login')
    method = request.method
    comment_id = request.form.get('comment_id')
    project_id = request.form.get('project_id')

    if method == 'GET':
        return redirect(url_for('disp_home'))

    if method == 'POST':
        del_comment(comment_id)
        return redirect(url_for('view_project', project_id=project_id, comment_empty=0) + "#comments_section")

    # except:
    #     return render_template("error.html")

@app.route("/delete_project", methods=['GET', 'POST'])
def delete_project():
    method = request.method
    project_id = request.form.get('project_id')

    if method == 'GET':
        return redirect(url_for('disp_home'))

    if method == 'POST':
        del_project(project_id)
        return redirect(url_for('gallery'))
    return

@app.route("/up_receiver", methods=["POST"])
def up_receiver():
    data = request.get_json()
    print(data[2:])
    upvote_comment(int(data[2:]), session['user_id'])

    ret = jsonify(data)
    return ret


@app.route("/down_reciever", methods=["POST"])
def down_reciever():
    data = request.get_json()
    print(data)
    downvote_comment(int(data[2:]), session['user_id'])

    ret = jsonify(data)
    return ret

@app.route("/neutral_receiver", methods=["POST"])
def neutral_receiver():
    data = request.get_json()
    print(data)
    neutralize_comment(int(data[2:]), session['user_id'])

    ret = jsonify(data)
    return ret

if __name__ == "__main__":  # false if this file imported as module
    # enable debugging, auto-restarting of server when this file is modified
    # FOR DEVWORK ONLY
    app.debug = True
    app.run()
    # FOR HOSTING ONLY
    # app.debug = False
    # app.run(host='0.0.0.0')
