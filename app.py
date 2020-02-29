from flask import Flask

from flask import render_template


app = Flask(__name__)


@app.route('/')
@app.route('/username/<name>')

def hello(name: str = None):
    try:
        return render_template("index.html", username=name)
    except Exception as e:
        return(str(e))


if __name__ == '__main__':
    app.run()