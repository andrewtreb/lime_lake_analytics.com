import mysql.connector

class database:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="andyt",
            password="@mHerst73",
            database="lime_lake_analytics"
        )

        self.cursor = self.mydb.cursor()

    def get_posts(self):
        self.cursor.execute("SELECT postid,title,author,post_text,thumbnail FROM blog_posts")
        return self.cursor.fetchall()
    
    def get_post(self, id):
        query = "SELECT postid,title,author,post_text FROM blog_posts WHERE postid = {}".format(id)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def create_post(self, title, author, post_text, thumbnail):
        baseSql = "INSERT INTO blog_posts(title, author, post_text, thumbnail) \
            VALUES (%s,%s,%s,%s)"
        vals = (title,author,post_text,thumbnail)
        
        self.cursor.execute(baseSql,vals)
        self.mydb.commit()


