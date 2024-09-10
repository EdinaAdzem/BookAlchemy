from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_models import Author, Book

# Create an instance of the Flask application
app = Flask(__name__)

# uri SQLite database library.sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'

# Initialize the SQLAlchemy object
db = SQLAlchemy()

# Bind the SQLAlchemy object to Flask app
db.init_app(app)


@app.route('/')
def home():
    return "test"

if __name__ == '__main__':
    app.run(debug=True)
