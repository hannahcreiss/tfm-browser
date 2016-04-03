# -*- encoding: utf-8 -*-
# begin

from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from todoapp import app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)



class Category (db.Model):
    __tablename__ = "category"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)


class Author (db.Model):
    __tablename__ = "author"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)


class Todo (db.Model):
    __tablename__ = "todo"
    id = db.Column('id', db.Integer, primary_key=True)
    category_id = db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
    author_id = db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
    description = db.Column('description', db.Unicode)
    creation_date = db.Column('creation_date', db.Date, default=datetime.utcnow)
    is_done = db.Column('is_done', db.Boolean, default=False)

    author = db.relationship('Author', foreign_keys=author_id)
    category = db.relationship('Category', foreign_keys=category_id)

class User(db.Model):
    __tablename__ = "user"
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False    

if __name__ == '__main__':
    manager.run()

# end
