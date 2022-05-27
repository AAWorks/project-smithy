# Specifications
1. Must be logged in to comment or upload, but can toggle anonymous for comments
2. Users with admin access (i.e. Mykolyk) can view comment and ratings sources
3. Ratings are anonymous, unless chosen not to be alongside a comment
4. Account page, view all public uploads that account has made
4.1. If it is your account or you are an admin account, view all uploads

# Database
Login Table
UserID | Passwords (Hash) + Salt | first | last | favorites | average_rating_given

Projects Table
Project_ID | Project_Title | Authors | Avg_Rating | 

Comments Table
Comment | Project_ID | UserID | Upvotes | Downvotes | Anonymous | 

Ratings Table
UserID | Project_ID | Rating |
