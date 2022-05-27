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
Project_ID | Project_Title | Authors | Avg_Rating | <br>

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