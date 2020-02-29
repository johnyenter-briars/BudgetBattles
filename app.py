from flask import Flask
from flask import request, redirect
from flask import render_template

from APIConnectionService import ApiConnectionService

app = Flask(__name__)

apiService = ApiConnectionService()

@app.route('/')
@app.route('/username/<name>')
def hello(name: str = None):
    
    withdrawls2 = apiService.GetAllWithdrawals("5e5a90faf1bac107157e0c50").get_withdrawals()
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