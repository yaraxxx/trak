import os
from sqlalchemy import Column, String, Integer, Date,  ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
import datetime
from sqlalchemy_json import mutable_json_type
# JSONB in Postgre
# https://www.compose.com/articles/faster-operations-with-the-jsonb-data-type-in-postgresql/
# https://amercader.net/blog/beware-of-json-fields-in-sqlalchemy/
from sqlalchemy.dialects.postgresql import JSONB


db = SQLAlchemy()


'''
Setup_db(app)
    To bind the flask application with the sqlalchemy service
'''


def setup_db(app):
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename
    variable to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


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
    __tablename__ = 'project'

    project_id = db.Column(Integer, primary_key=True)
    project_name = db.Column(String, nullable=False)
    target_end_date = db.Column(Date, nullable=False)
    actual_end_date = db.Column(Date, nullable=True)
    label = db.Column(mutable_json_type(dbtype=JSONB, nested=True))
    created_on = db.Column(Date, nullable=False)
    created_by = db.Column(Integer, nullable=False)
    modified_on = db.Column(Date, nullable=True)
    modified_by = db.Column(Integer, nullable=True)
    issues = db.relationship('Issue', backref='project',
                             cascade='all, delete-orphan')

    '''
    short()
        short form representation of only editable attributes
    '''

    def short(self):
        return {'project_id': self.project_id,
                'project_name': self.project_name,
                'target_end_date': self.target_end_date,
                'actual_end_date': self.actual_end_date,
                'label': self.label}

    '''
    long()
        long form representation of the whole model
    '''

    def long(self):
        return{'project_id': self.project_id,
               'project_name': self.project_name,
               'target_end_date': self.target_end_date,
               'actual_end_date': self.actual_end_date,
               'label': self.label,
               'created_on': self.created_on,
               'created_by': self.created_by,
               'modified_on': self.modified_on,
               'modified_by': self.modified_by}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def close(self):
        db.session.close()

    def __repr__(self):
        return json.dumps(self.long())


# Bridge table
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
    __tablename__ = 'assignedprojects'

    user_id = db.Column(Integer, ForeignKey(
        "user.user_id"), primary_key=True, nullable=False)
    project_id = db.Column(Integer, ForeignKey(
        "project.project_id"), primary_key=True, nullable=False)
    user_role = db.Column(String, nullable=False)

    '''
    long()
        long form representation of the whole model
    '''

    def long(self):
        return {'user_id': self.user_id,
                'project_id': self.project_id,
                'user_role': self.user_role, }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def close(self):
        db.session.close()

    def __repr__(self):
        return json.dumps(self.long())


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
    __tablename__ = 'user'

    user_id = db.Column(Integer, primary_key=True)
    user_name = db.Column(String, nullable=False)
    username = db.Column(String, nullable=False, unique=True)
    created_on = db.Column(Date, nullable=False)
    projects = db.relationship(
        'project', secondary=AssignedProjects, backref=db.backref('user', lazy='dynamic'))

    '''
    short()
        short form representation of only editable attributes
    '''

    def short(self):
        return {'user_id': self.project_id,
                'user_name': self.project_name}

    '''
    long()
        long form representation of the whole model
    '''

    def long(self):
        return{'user_id': self.project_id,
               'user_name': self.project_name,
               'username': self.username,
               'created_on': self.created_on}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def close(self):
        db.session.close()

    def __repr__(self):
        return json.dumps(self.long())


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


class Issue(db.Model):
    __tablename__ = 'issue'
    va_version_columns = ['last_modification_on']

    issue_id = db.Column(Integer, primary_key=True)
    issue_summary = db.Column(String, nullable=False)
    issue_description = db.Column(String, nullable=True)
    assigned_to = db.Column(Integer, nullable=True)
    status = db.Column(String, nullable=False)
    # deal with it in the form file where you will list lables json from Projects table
    label = db.Column(String, nullable=True)
    priority = db.Column(String, nullable=False)
    target_resolution_date = db.Column(Date, nullable=True)
    actual_resolution_date = db.Column(Date, nullable=True)
    progress = db.Column(String, nullable=True)  # deal with it in form.py
    resolution_summary = db.Column(String, nullable=True)
    created_on = db.Column(Date, nullable=False)
    created_by = db.Column(Integer, nullable=False)
    last_modification_on = db.Column(Date, nullable=False)
    last_modification_by = db.Column(Integer, nullable=False)
    project = db.Column(Integer, ForeignKey(
        "project.project_id"), nullable=False)

    '''
    short()
        short form representation of only editable attributes
    '''

    def short(self):
        return {'issue_id': self.issue_id,
                'issue_summary': self.issue_summary,
                'issue_description': self.issue_description,
                'assigned_to': self.assigned_to,
                'status': self.status,
                'label': self.label,
                'priority': self.priority,
                'target_resolution_date': self.target_resolution_date,
                'actual_resolution_date': self.actual_resolution_date,
                'progress': self.progress,
                'resolution_summary': self.resolution_summary,
                'last_modification_on': self.last_modification_on,
                'last_modification_by': self.last_modification_by}

    '''
    long()
        long form representation of the whole model
    '''

    def long(self):
        return{'issue_id': self.issue_id,
               'issue_summary': self.issue_summary,
               'issue_description': self.issue_description,
               'assigned_to': self.assigned_to,
               'status': self.status,
               'label': self.label,
               'priority': self.priority,
               'target_resolution_date': self.target_resolution_date,
               'actual_resolution_date': self.actual_resolution_date,
               'progress': self.progress,
               'resolution_summary': self.resolution_summary,
               'created_on': self.created_on,
               'created_by': self.created_by,
               'last_modification_on': self.last_modification_on,
               'last_modification_by': self.last_modification_by}

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()

    def close(self):
        db.session.close()

    def __repr__(self):
        return json.dumps(self.long())
