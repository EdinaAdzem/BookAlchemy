import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

# Create an instance of the Flask app
app = Flask(__name__)

# Configure the SQLite database URI
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'library.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the SQLAlchemy object to the Flask app
db.init_app(app)

# Create once
#with app.app_context():
    #db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
