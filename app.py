from flask import Flask

from flask import request, redirect
from flask import render_template
from APIConnectionService import ApiConnectionService
from database_service import *

db_operations = DatabaseService()

app = Flask(__name__)
apiService = ApiConnectionService()
@app.route('/')
@app.route('/username/<name>')
def hello(name: str = None):
    try:
        return render_template("index.html", username=name)
    except Exception as e:
        return(str(e))

@app.route('/databasetest')
def db_test():
    print(db_operations.get_user(100))
    print(db_operations.get_user_record(100))
    try:
        return render_template("index.html", username=name)
    except Exception as e:
        return(str(e))
        
@app.route('/signin', methods = ['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    print("The username address is '" + username + "'" + password)
    return redirect('/')

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/signup', methods = ['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    print("The username address is '" + username + "'" + password)
    return redirect('/')

def initialize_database() -> sqlite3.Connection:
    """Create a sqlite3 database stored in memory with two tables to hold
    users, records and history. Returns the connection to the created database."""
    with sqlite3.connect("bank_buds.db") as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS user(
            userId INTEGER PRIMARY KEY NOT NULL,
            userName TEXT NOT NULL,
            userPass TEXT NOT NULL)""")

        conn.execute("""CREATE TABLE IF NOT EXISTS user_record(
            rec_id INTEGER REFERENCES user NOT NULL,
            wins INTEGER NOT NULL,
            losses INTEGER NOT NULL)""")

        conn.execute("""CREATE TABLE IF NOT EXISTS challenge_history(
            challenge_id INTEGER NOT NULL,
            challenge_winner REFERENCES user NOT NULL,
            challenge_loser REFERENCES user NOT NULL,
            is_active NUMERIC NOT NULL )""")  
        return conn 

if __name__ == '__main__':
    initialize_database()
    app.run()