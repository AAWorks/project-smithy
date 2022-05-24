# Project Reviewal
### Team Jimin - Alejandro Alonso, Noakai Aronesty, Justin Zou, Ivan Lam

# Specifications
1. Must be logged in to comment or upload, but can toggle anonymous for comments
2. Users with admin access (i.e. Mykolyk) can view comment and ratings sources
3. Ratings are anonymous, unless chosen not to be alongside a comment
4. Account page, view all public uploads that account has made
4.1. If it is your account or you are an admin account, view all uploads

# Database
__Login Table__  
Username | Passwords (Hash) + Salt | Class_Ranking |

__Projects Table__  
Project_ID | Project_Title | Authors | Avg_Rating | 

__Comments Table__  
Comment | Project_ID | Username | Upvotes | Downvotes | Anonymous | 

__Ratings Table__  
Username | Project_ID | Rating |
