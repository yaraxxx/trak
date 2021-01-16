
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


if __name__ == '__main__':
    app.run()
