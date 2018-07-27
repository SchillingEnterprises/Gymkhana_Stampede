from flask import Flask
from flask import render_template


app = Flask(__name__)


# Default
@app.route('/')
@app.route('/<name>')
def index(name='SoMe Media'):
    return render_template("layout.html", name=name)


app.run(debug=True, port=8000, host='0.0.0.0')