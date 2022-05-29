from flask import url_for
from notanorm import SqliteDb

DB_FILE = "project_reviewal.db"

def upload_project(title, image, team_name, pmID, devoIDs, tags, repo, intro, descrip, rating, hosted_loc):
    db = SqliteDb(DB_FILE)

    devos = "|".join([devoID.replace("|", "") for devoID in devoIDs])
    tags = "|".join([tag.replace("|", "") for tag in tags])
    db.insert("projects", title=title, image=image, team_name=team_name, pmID=pmID, devoIDs=devos, tags=tags, repo=repo, intro=intro, descrip=descrip, rating=rating, hosted_loc=hosted_loc)

def get_project_details(project_id):
    db = SqliteDb(DB_FILE)
    
    project = db.select("projects", project_id=project_id)[0]
    details = project
    details['devoIDs'] = project['devos'].split("|")
    details['tags'] = project['tags'].split("|")

    return details

def get_project_snapshot(project_id):
    db = SqliteDb(DB_FILE)

    project = db.select("projects", project_id=project_id)[0]
    snapshot = {'image': project['image'], 'title': project['title'], 'team': project['team_name'], 'tags': project['tags'].split("|"), 'intro': project['intro'], 'project_id': project['project_id']}

    return snapshot

def edit_project_info(projectID, column_toEdit, new_val):
    db = SqliteDb(DB_FILE)

    db.update("projects", where={"project_id": projectID}, upd={column_toEdit: new_val})