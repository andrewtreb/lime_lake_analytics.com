from flask import Flask, render_template, url_for
from flaskext.markdown import Markdown
from lla.database import database
from lla.weatherData import visuals
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import subprocess

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
    viz = visuals()
    graphJson = viz.current_temp_ind()
    last_hour = viz.data_last_hour()

    return render_template('weatherData.html', graphJSON=graphJson, last_hour=last_hour)

@app.route('/weatherDataTest')
def weatherDataTest():
    src = "https://streamlit.limelakeanalytics.com/"
    return render_template('iframe.html',src = src)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=False)