# Specifications
1. Must be logged in to comment or upload, but can toggle anonymous for comments
2. Users with admin access (i.e. Mykolyk) can view comment and ratings sources
3. Ratings are anonymous, unless chosen not to be alongside a comment
4. Account page, view all public uploads that account has made
4.1. If it is your account or you are an admin account, view all uploads
<br>
# Database
Login Table<br>
UserID | Passwords (Hash) + Salt | first | last | favorites | average_rating_given<br>

Projects Table<br>
project_id | title | team_name | pmID | devoIDs | tags | repo | descrip1 | descrip2 | avg_rating | comments | hosted | hosted_loc <br>

Comments Table<br>
Comment | Project_ID | UserID | Upvotes | Downvotes | Anonymous | <br>

Ratings Table<br>
UserID | Project_ID | Rating |<br>

# Color Palette
Purpleish thing:<br>
#5a4ae3<br>
rgba(90,74,227,255)<br><br>

Greenish thing:<br>
#49a18c<br>
rgba(73,161,140,255)<br><br>

Noakai is using this:<br>
#237677<br>
rgba(35,118,119, 150)<br>
since the other green is too bright imo (we can test both)

<br><br>
project.html needs the following:
title, date_uploaded, team_name, tags, team_name, pm_id, pm_name, devos (each is a dictionary of id and name), hosted (boolean), repo_link, hosted_loc, comments (list of comments --> each comment is a dictionary of text, devo_pfp, devo_id, and devo_name), project_descrip_1, project_descrip_2

<br>
Gravatar API rundown: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vi-profile-page-and-avatars
