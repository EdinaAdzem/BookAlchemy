import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from datetime import datetime

# Create an instance of the Flask app
app = Flask(__name__)

# Configure the SQLite database URI
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'library.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'WORKDARNIT'

# Bind the SQLAlchemy object to the Flask app
db.init_app(app)


# Create once
# with app.app_context():
# db.create_all()

@app.route('/')
def home():
    books = Book.query.all()  # always query all the books
    return render_template('home.html', books=books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date_str = request.form.get('birth_date')
        date_of_death_str = request.form.get('date_of_death')
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d') if birth_date_str else None
        date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d') if date_of_death_str else None
        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        try:
            db.session.add(new_author)
            db.session.commit()
            flash('Author added successfully!', 'success')
            return redirect(url_for('add_author'))
        except Exception as e:
            db.session.rollback()  # roll back in case of issues like sevice down
            flash(f'Author could not be added, please check the services: {e}', 'danger')

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    authors = Author.query.all()

    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        new_book = Book(title=title, author_id=author_id)
        try:
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!', 'success')
            return redirect(url_for('add_book'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding book: {e}', 'danger')
    return render_template('add_book.html', authors=authors)


if __name__ == "__main__":
    app.run(debug=True)
