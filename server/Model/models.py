import os
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy
import json
import datetime
from sqlalchemy_json import mutable_json_type
# For versioning
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint

import versionalchemy as va
from versionalchemy.models import VAModelMixin, VALogMixin

db = SQLAlchemy()

'''
Setup_db(app)
    To bind the flask application with the sqlalchemy service
'''


def setup_db(app):
    db.app = app
    db.init_app(app)
    engine = create_engine(app.config[SQLALCHEMY_DATABASE_URI])
    Base = declarative_base(bind=engine)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename
    variable to have multiple verisons of a database
'''
# def db_drop_and_create_all():
#     db.drop_all()
#     db.create_all()

'''
Projects
tracks all current projects
    -> insert()
        inserts a new record into the database
        EXAMPLE
            project = Project(......)
            project.insert()
    -> delete()
        deletes a record in the database
        the record must exist in the database
        EXAMPLE
            project = Project(......)
            project.delete()
    -> update()
        updates a record in the database
        the record must exist in the database
        EXAMPLE
            project = Project.query.filter(Project.id == id).one_or_none()
            project.title = '-----'
            project.update()
'''


class Project(db.Model):
    __tablename__ = 'Project'

    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String, nullable=False)
    target_end_date = db.Column(db.Date, nullable=False)
    actual_end_date = db.Column(db.Date, nullable=True)
    label = db.Column(mutable_json_type(dbtype=JSONB, nested=True))
    created_on = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.Integer, ForeignKey(
        "User.user_id"), nullable=False)
    modified_on = db.Column(db.Date, nullable=True)
    modified_by = db.Column(db.Integer, ForeignKey(
        "User.user_id"), nullable=True)


'''
User
contains information about who can be assigned to handle issues
    -> insert()
        inserts a new record into the database
       
    -> delete()
        deletes a record in the database
        the record must exist in the database
      
    -> update()
        updates a record in the database
        the record must exist in the database
        
'''


class User(db.Model):
    __tablename__ = 'User'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    created_on = db.Column(db.Date, nullable=False)


'''
AssignedProjects
junction table
    -> insert()
        inserts a new record into the database
       
    -> delete()
        deletes a record in the database
        the record must exist in the database
      
    -> update() ONLY UPDATE ROLE ATTRIBUTE
        updates a record in the database
        the record must exist in the database
        
'''


class AssignedProjects(db.Model):
    __tablename__ = 'AssignedProjects'

    user_id = db.Column(db.Integer, ForeignKey(
        "User.user_id"), unique=True, nullable=False)
    project_id = db.Column(db.Integer, ForeignKey(
        "Project.project_id"), unique=True, nullable=False)
    user_role = db.Column(db.String, nullable=False)


'''
Issues
tracks all information about an issue
    -> insert()
        inserts a new record into the database
       
    -> delete()
        deletes a record in the database
        the record must exist in the database
      
    -> update()
        updates a record in the database
        the record must exist in the database
        
'''


class Issue(db.Model, Base):
    __tablename__ = 'Issue'

    issue_id = db.Column(db.Integer, primary_key=True)
    issue_summary = db.Column(db.String, nullable=False)
    issue_description = db.Column(db.String, nullable=True)
    assigned_to = db.Column(db.Integer, ForeignKey(
        "User.user_id"), nullable=True)
    status = db.Column(db.String, nullable=False)
    # deal with it in the form file where you will list lables json from Projects table
    label = db.Column(db.String, nullable=True)
    priority = db.Column(db.String, nullable=False)
    target_resolution_date = db.Column(db.Date, nullable=True)
    actual_resolution_date = db.Column(db.Date, nullable=True)
    progress = db.Column(db.String, nullable=True)  # deal with it in form.py
    resolution_summary = db.Column(db.String, nullable=True)
    created_on = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.Integer, ForeignKey(
        "User.user_id"), nullable=False)
    modified_on = db.Column(db.Date, nullable=True)
    modified_by = db.Column(db.Integer, ForeignKey(
        "User.user_id"), nullable=True)


'''
ChangesHistory
tracks changes made to an issue
    -> insert()
        inserts a new record into the database
       
    -> delete() In case the issue was removed
        deletes a record in the database
        the record must exist in the database
        
'''


class ChangesHistory(db.Model):
    __tablename__ = 'ChangesHistory'
