
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time


# app = Flask(__name__, instance_relative_config=True)
# app.config.from_object('config')
# app.config.from_pyfile('config.py')

app = Flask(__name__)


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


if __name__ == '__main__':
    app.run(debug=True)
