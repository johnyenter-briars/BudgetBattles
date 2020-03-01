from flask import Flask

from flask import request, redirect
from flask import render_template
from ReportingService import ReportingService
from APIConnectionService import ApiConnectionService
from database_service import *
rp = ReportingService()

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
    test_dict = {"joe": 0, "nill": 1}
    #print(db_operations.add_user(100, "hoe", "hoePass"))
    #print(db_operations.add_user(200, "joe", "joePass"))
    print(db_operations.get_user(100))
    print(db_operations.get_user_record(100))
    chall_id = db_operations.create_challenge("joe", "bill")
    print(db_operations.get_challenge(chall_id))
    print("--pre-update above--")
    print(chall_id)
    print(db_operations.update_challenge_status(chall_id, test_dict))
    print(db_operations.get_challenge(chall_id))
    try:
        return render_template("index.html", username=name)
    except Exception as e:
        return(str(e))
        
@app.route('/signin', methods = ['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    print(db_operations.get_user(username))
    if db_operations.get_user(username) == []:
        return redirect('/register')
    else:
        return render_template("home.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/signup', methods = ['POST'])
def signup():
    lastName = request.form['lastName']
    firstName = request.form['firstName']
    username = request.form['username']
    password = request.form['password']
    user_id = hashlib.sha1(b'combo_str').hexdigest()
    print(user_id)
    db_operations.add_user(firstName, lastName, username, password)
    print(db_operations.get_user(username))
    return redirect('/')


@app.route('/reportingtest')
def reporting_test():
    #data = rp.getCurentHistory('5e5a90faf1bac107157e0c50')
    #data = rp.getCurentHistory('5e5af922f1bac107157e0c7f')
    data = rp.getCurentHistory('5e5afcdbf1bac107157e0c8e')
    try:
        return render_template("index.html", username=name)
    except Exception as e:
        return(str(e))

def initialize_database() -> sqlite3.Connection:
    """Create a sqlite3 database stored in memory with two tables to hold
    users, records and history. Returns the connection to the created database."""
    with sqlite3.connect("bank_buds.db") as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS user(
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            userName TEXT NOT NULL,
            userPass TEXT NOT NULL)""")

        conn.execute("""CREATE TABLE IF NOT EXISTS user_record(
            rec_id TEXT REFERENCES user NOT NULL,
            wins INTEGER NOT NULL,
            losses INTEGER NOT NULL)""")

        conn.execute("""CREATE TABLE IF NOT EXISTS challenge_history(
            challenge_id INTEGER NOT NULL,
            challenge_starter TEXT REFERENCES user NOT NULL,
            challenge_opponent TEXT REFERENCES user NOT NULL,
            challenge_winner TEXT REFERENCES user NOT NULL,
            challenge_loser TEXT REFERENCES user NOT NULL,
            is_active INTEGER NOT NULL )""")  
        return conn 

if __name__ == '__main__':
    initialize_database()
    app.run()