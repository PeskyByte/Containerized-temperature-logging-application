from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
import requests
from functools import wraps

app = Flask(__name__)
app.secret_key = '5678'

def get_db_connection():
    connection = mysql.connector.connect(
        host='db',
        user='root',
        password='rootpassword',
        database='tempdb'
    )
    return connection

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
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
@login_required
def submit_temperature():
    temperature = request.form['temperature']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO temperature_readings (reading) VALUES (%s)", (temperature,))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')