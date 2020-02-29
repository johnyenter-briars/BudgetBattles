from flask import Flask
from flask import request, redirect
from flask import render_template
from ReportingService import ReportingService

from APIConnectionService import ApiConnectionService
from database_service import *
rp = ReportingService()

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

@app.route('/reportingtest')
def reporting_test():
    data = rp.getCurentHistory('5e5a90faf1bac107157e0c50')
    try:
        return render_template("index.html", username=name)
    except Exception as e:
        return(str(e))

if __name__ == '__main__':
    app.run()