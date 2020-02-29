from flask import Flask
from flask import request, redirect
from flask import render_template

from APIConnectionController import ApiConnectionController


app = Flask(__name__)

apiController = ApiConnectionController()

@app.route('/')
@app.route('/username/<name>')
def hello(name: str = None):
    print(apiController.GetAccountInformation("5e5a180af1bac107157e0b7d").get_balance())

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