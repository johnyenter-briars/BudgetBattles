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
    if db_operations.get_user(username) == []:
        return redirect('/register')
    else:
        return redirect("/home/{0}".format(username))

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/home/challenge')
def route():
    return render_template("challenge.html")

#TEMP ROUTE FOR TESTING - DELETE FOR FINAL PRODUCT
@app.route('/home/<user_name>')
def home(user_name:str = None):
    print(user_name)
    customer_id = db_operations.get_user(user_name)[0][0]
    print(customer_id)

    opponents = db_operations.get_user_challenges(user_name)
    if len(opponents) == 0:
        return redirect("/challenge")

    opponent_username = opponents[0][2]
    print(opponent_username)
    opponent_id = db_operations.get_user(opponent_username)[0][0]

    rp.generateUserHistory(customer_id)
    rp.generateUserHistory(opponent_id)

    user_balance_path = "/static/balance_{0}.png".format(customer_id)
    user_withdrawal_path = "/static/withdrawal_{0}.png".format(customer_id)

    opponent_balance_path = "/static/balance_{0}.png".format(opponent_id)
    opponent_withdrawal_path = "/static/withdrawal_{0}.png".format(opponent_id)


    return render_template("home.html", user_withdrawal_graph=user_balance_path, user_balance_graph=user_withdrawal_path, 
                            opponent_withdrawal_path=opponent_withdrawal_path,opponent_balance_path=opponent_balance_path, 
                            user_full_name=user_name, opponent_full_name=opponent_username)

@app.route('/home/challenge', methods = ['POST'])
def challenge():
    challengeStarter = request.form['challengeStarter']
    challengeOpponent = request.form['challengeOpponent']
    goal = request.form['goal']
    chall_id = db_operations.create_challenge(challengeStarter,challengeOpponent,goal)
    return redirect("/home/{0}".format(challengeStarter))

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
    if customer_id == None:
        return redirect('/error')
    if checkAccount == None:
        return redirect('/error')
    balance = db_operations.get_user_balance(customer_id)
    db_operations.add_user(customer_id, firstName, lastName, username,password,balance)
    return redirect('/')

@app.route('/customeridtest')
def customeridtest():
    # expected return if you're running on john's api key is: 5e5b17c4f1bac107157e0ca1
    print(apiService.SearchForCustomerId("Paul", "Blart"))
    try:
        return render_template("index.html")
    except Exception as e:
        return(str(e))

@app.route('/reportingtest<username>')
def reporting_test(userName:str = None):
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
            is_active INTEGER NOT NULL,
            goal INTEGER NOT NULL)""")

        return conn 

if __name__ == '__main__':
    initialize_database()
    app.run()