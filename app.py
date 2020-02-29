from flask import Flask
from flask import request, redirect
from flask import render_template

from APIConnectionService import ApiConnectionService
from database_service import *

app = Flask(__name__)

apiService = ApiConnectionService()
dbConnection = None
dbService = DatabaseService2()



@app.route('/')
@app.route('/username/<name>')
def hello(name: str = None):
    try:
        return render_template("index.html", username=name)
    except Exception as e:
        return(str(e))

@app.route('/databasetest')
def db_test():
    print(dbService.get_user2(100))
    
    try:
        return render_template("index.html", username=name)
    except Exception as e:
        return(str(e))

@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['email']
    print("The email address is '" + email + "'")
    return redirect('/')

if __name__ == '__main__':
    app.run()