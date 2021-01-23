
from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
import time
from flask_cors import CORS
from .. import config
from server.models import db, db_drop_and_create_all, setup_db, Project, AssignedProjects, User, Issue
from flask_migrate import Migrate


def create_app():
    # App Config.
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    setup_db(app)
    migrate = Migrate(app, db)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Origin', '*')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, DELETE, PATCH, OPTIONS')
        return response
    '''
    uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START THE DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    db_drop_and_create_all()

    @app.route('/time')
    def get_current_time():
        return {'time': time.time()}
    return app


app = create_app()

if __name__ == '__main__':
    app.run()
