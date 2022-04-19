from database import database

db = database()

post = '''
<img src="https://drive.google.com/uc?export=view&id=1sjx6NJgKZ-40-IwONxITp7pdiVC15dwU" width = 80%/>

### Testing Markdown in Blog
&emsp;Testing markdown in website. Testing it in a new line when it goes long enough.
Continuing to write to make it look good.

'''

db.create_post("Markdown Test","Andrew Trzebiatowski",post, \
    "https://drive.google.com/uc?export=view&id=1sjx6NJgKZ-40-IwONxITp7pdiVC15dwU")



# db.cursor.execute(" \
# CREATE TABLE IF NOT EXISTS blog_posts ( \
#     postid int NOT NULL AUTO_INCREMENT PRIMARY KEY, \
#     title varchar(255), \
#     author varchar(255), \
#     post_text text, \
#     thumbnail text, \
#     posted_time timestamp DEFAULT CURRENT_TIMESTAMP \
# ) \
# ")