from flask import Flask, render_template, url_for
from flaskext.markdown import Markdown
from lla.database import database
from datetime import datetime
app = Flask(__name__)
Markdown(app)
db = database()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact-info')
def contact():
    return render_template('contact.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html', data=db.get_posts())

@app.route('/blog/<id>')
def blog(id):
    return render_template('blog.html', data=db.get_post(id))

@app.route('/project/weatherData')
def weatherData():
    return render_template('weatherData.html', data=db.get_lastHourWeatherData())

def temp():
    df = db.get_allWeatherData()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=False)