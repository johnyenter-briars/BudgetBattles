from flask import Flask

from flask import request, redirect
from flask import render_template
from APIConnectionService import ApiConnectionService
app = Flask(__name__)
apiService = ApiConnectionService()
@app.route('/')
@app.route('/username/<name>')
def hello(name: str = None):
    try:
        return render_template("index.html", username=name)
    except Exception as e:
        return(str(e))
@app.route('/signup', methods = ['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    print("The username address is '" + username + "'" + password)
    return redirect('/')
if __name__ == '__main__':
    app.run()