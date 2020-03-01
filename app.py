from flask import Flask

from flask import request, redirect
from flask import render_template
#from ReportingService import ReportingService
from APIConnectionService import ApiConnectionService
from database_service import *


#rp = ReportingService()

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
    db_operations.add_user("A", "B", "murt", "1234")
    db_operations.add_user("A", "B", "elona", "1234")
    db_operations.add_user("A", "B", "pat", "1234")

    chall_id1 = db_operations.create_challenge("murt", "elona")
    chall_id2 = db_operations.create_challenge("murt", "pat")
    chall_id3 = db_operations.create_challenge("elona", "murt")
    chall_id4 = db_operations.create_challenge("elona", "pat")
    chall_id5 = db_operations.create_challenge("pat", "murt")
    chall_id6 = db_operations.create_challenge("pat", "elona")
    print("--CHALLENGE MURT--")
    print(db_operations.get_user_challenges("murt"))
    print("--CHALLENGE ELONA--")
    print(db_operations.get_user_challenges("elona"))
    print("--CHALLENGE PAT--")
    print(db_operations.get_user_challenges("pat"))
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

@app.route('/challenge')
def route():
    return render_template("challenge.html")

#TEMP ROUTE FOR TESTING - DELETE FOR FINAL PRODUCT
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/challenge', methods = ['POST'])
def challenge():
    challengeStarter = request.form['challengeStarter']
    challengeOpponent = request.form['challengeOpponent']
    chall_id = db_operations.create_challenge(challengeStarter,challengeOpponent)
    print(db_operations.get_challenge(chall_id))
    return redirect('/home')

@app.route('/index')
def index():
    return render_template("index.html")
    
@app.route('/error')
def error():
    return render_template("error.html")

@app.route('/signup', methods = ['POST'])
def signup():
    lastName = request.form['lastName']
    firstName = request.form['firstName']
    username = request.form['username']
    password = request.form['password']
    customer_id = apiService.SearchForCustomerId(firstName,lastName)
    checkAccount = apiService.GetAccountInformation(customer_id)
    print(customer_id)
    if customer_id == None:
        return redirect('/error')
    if checkAccount == None:
        return redirect('/error')
    balance = db_operations.get_user_balance(customer_id)
    db_operations.add_user(customer_id, firstName, lastName, username,password,balance)
    print(db_operations.get_user(username))
    return redirect('/')

@app.route('/customeridtest')
def customeridtest():
    # expected return if you're running on john's api key is: 5e5b17c4f1bac107157e0ca1
    print(apiService.SearchForCustomerId("Paul", "Blart"))
    try:
        return render_template("index.html")
    except Exception as e:
        return(str(e))

@app.route('/reportingtest')
def reporting_test():
    #data = rp.getCurentHistory('5e5a90faf1bac107157e0c50')
    #data = rp.getCurentHistory('5e5af922f1bac107157e0c7f')
    user_id = "5e5afcdbf1bac107157e0c8e"
    opponent_id = "5e5af922f1bac107157e0c7f"
    rp.generateUserHistory(user_id)
    rp.generateUserHistory(opponent_id)

    user_1_path = "static/balance_{0}.png".format(user_id)
    user_2_path = "static/balance_{0}.png".format(opponent_id)

    try:
        return render_template("test_reporting.html", path_to_user_image = user_1_path, path_to_opponent_image=user_2_path)
    except Exception as e:
        return(str(e))

def initialize_database() -> sqlite3.Connection:
    """Create a sqlite3 database stored in memory with two tables to hold
    users, records and history. Returns the connection to the created database."""
    with sqlite3.connect("bank_buds.db") as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS user(
            customer_id TEXT NOT NULL,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            userName TEXT NOT NULL,
            userPass TEXT NOT NULL,
            balance INTEGER NOT NULL)""")

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