from flask import Flask
from flask import request, redirect
from flask import render_template

from APIConnectionController import ApiConnectionService

app = Flask(__name__)

apiService = ApiConnectionService()

@app.route('/')
@app.route('/username/<name>')
def hello(name: str = None):
    withdrawls = apiService.GetAllWithdrawals("5e5a89c3f1bac107157e0c3b").get_withdrawals()
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