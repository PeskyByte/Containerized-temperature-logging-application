from flask import Flask, render_template, request, redirect, url_for, session
import pymongo
import requests
from functools import wraps

app = Flask(__name__)
app.secret_key = '1234'

def get_mongo_connection():
    client = pymongo.MongoClient("mongodb://mongo:27017/")
    return client.analytics_db

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        response = requests.post('http://auth:5002/authenticate', json={
            'username': username,
            'password': password
        })
        
        if response.status_code == 200:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return "Invalid credentials", 401
    
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    mongo_db = get_mongo_connection()
    latest_analytics = mongo_db.temperature_analytics.find_one(sort=[("timestamp", -1)])
    return render_template('analytics.html', analytics=latest_analytics)

if __name__ == '__main__':
    app.run(host='0.0.0.0')