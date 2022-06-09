from flask import url_for
from notanorm import SqliteDb
import datetime

DB_FILE = "project_reviewal.db"

def upload_project(title, image, team_name, pmID, devoIDs, tags, repo, intro, descrip, rating, hosted_loc, team_flag):
    db = SqliteDb(DB_FILE)

    devos = "|".join(devoIDs)
    tags = "|".join(tags)
    db.insert("projects", title=title, image=image, team_name=team_name, pmID=pmID, devoIDs=devos, tags=tags, repo=repo, intro=intro, descrip=descrip, rating=rating, hosted_loc=hosted_loc, team_flag=team_flag)

    project = db.select("projects", title=title, team_name=team_name, intro=intro)[-1]
    return project

def get_project_details(project_id):
    db = SqliteDb(DB_FILE)
    
    project = db.select("projects", project_id=project_id)[0]
    details = project
    details['devoIDs'] = project['devoIDs'].split("|")
    details['tags'] = project['tags'].split("|")

    return details

def get_project_snapshot(project_id):
    db = SqliteDb(DB_FILE)

    project = db.select("projects", project_id=project_id)[0]
    snapshot = {'pmID': project['pmID'], 'tot_rating': project['rating'], 'image': project['image'], 'title': project['title'], 'team': project['team_name'], 'tags': project['tags'].split("|"), 'summary': project['intro'], 'project_id': project['project_id'], 'avg_rating': getAvgRating(project['project_id'])}

    return snapshot

def edit_project_info(projectID, column_toEdit, new_val):
    db = SqliteDb(DB_FILE)

    db.update("projects", where={"project_id": projectID}, upd={column_toEdit: new_val})

def get_all_projects():
    db = SqliteDb(DB_FILE)

    return db.select('projects')

def get_all_project_ids():
    projects = get_all_projects()
    ids = []

    for project in projects:
        ids.append(project['project_id'])
    
    return ids

def delete_project(project_id):
    db = SqliteDb(DB_FILE)
    db.delete("projects", project_id=project_id)

def clear_projects_table():
    check = input("YOU ARE ABOUT TO DELETE EVERY ENTRY IN THE PROJECTS TABLE OF THE DATABASE. CONTINUE (Y/N): ")
    if check != "Y":
        return False
    db = SqliteDb(DB_FILE)
    db.delete_all("projects")


def updateRating(project_id,ratings,user_id):
    db = SqliteDb(DB_FILE)
    project = db.select("projects", project_id=project_id)[0]
    counter = db.select("ratings", project_id=project_id)
    if db.select("ratings", project_id=project_id, user_id=user_id):
        sum = float(ratings)
        sum -= db.select("ratings", project_id=project_id, user_id=user_id)[0]["rating"]
        db.update("projects", where={"project_id": project_id}, upd = {"rating": project["rating"] + sum})
        db.update("ratings", where={"project_id": project_id, "user_id":user_id}, upd={"rating": ratings})
    else:
        db.insert("ratings", project_id=project_id, user_id=user_id, rating = ratings)
        sum = project["rating"] 
        sum += float(ratings)
        db.update("projects", where={"project_id": project_id}, upd = {"rating": sum})
    # print(len(counter))
    
    # counter = project["ratingCounter"]
    # counter += 1
    
   
    # ,"ratingCounter":counter}


def getAvgRating(project_id):
    db = SqliteDb(DB_FILE)
    project = db.select("projects", project_id=project_id)[0]
    counter = db.select("ratings", project_id=project_id)
    s = project["rating"]
    if (len(counter) > 0):
        return s/len(counter)
    return 0

def get_project_comments(project_id):
    db = SqliteDb(DB_FILE)
    return [comment for comment in db.select("comments", project_id=project_id) if comment['user_id'] != 1]

def get_admin_comment(project_id):
    db = SqliteDb(DB_FILE)
    return [comment for comment in db.select("comments", project_id=project_id) if comment['user_id'] == 1]

def get_average_rating_given(user_id):
    db = SqliteDb(DB_FILE)
    user_ratings = db.select('ratings', user_id=user_id)
    avg_rating = 0
    tot_ratings = 0

    if user_ratings:
        for rating in user_ratings:
            avg_rating += rating['rating']
            tot_ratings += 1
    else:
        return "N/A"
    
    return round(float(avg_rating) / float(tot_ratings), 1)

#def get_projects_by_devo_year():
#     db = SqliteDb(DB_FILE)
#     projects, all_projects = [], [project['project_id'] for project in db.select("projects")]

#     for pid in all_projects:
#         temp_project = get_project_snapshot(pid)
#         user_id = int(temp_project['pmID'].split("#")[1])
#         pm_year = db.select("users", user_id=user_id)[0]["year"]
#         temp_project["year"] = pm_year
        
#         projects.append(temp_project)

#     return sorted(projects, key=lambda d: d['year'])

def get_projects_by_star_rating():
    db = SqliteDb(DB_FILE)
    projects=[]
    project_ids = [project['project_id'] for project in db.select("projects")]
    for pid in project_ids:
        projects.append(get_project_snapshot(pid))

    return sorted(projects, key=lambda d: d['tot_rating'])

def projects_with_tag(tag):
    db = SqliteDb(DB_FILE)
    return [get_project_snapshot(project['project_id']) for project in db.select('projects') if tag in project['tags'].split("|")]