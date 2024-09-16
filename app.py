import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from datetime import datetime
import requests

""" To run the application  - run on terminal the following
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
"""

# Create an instance of the Flask app
app = Flask(__name__)

# Define the OMDB API URL and key
# URL_API = "http://www.omdbapi.com/"
# API_KEY = "c3bb5c1c"

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
    """Home route function that handles the query and api calls to get the books info """
    books = Book.query.all()  # Query all books from the database

    # remove the api call
    books_with_covers = []
    for book in books:
        books_with_covers.append({
            'id': book.id,
            'title': book.title,
            'author': book.author.name,
            'cover': 'static/default_image.jpg'
        })

    return render_template('home.html', books=books_with_covers)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """add_author route utilizes the post request and inserts the data to the database"""
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
    """add_book route utilizes the post request and inserts the data to the database"""
    authors = Author.query.all()

    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        isbn = request.form.get('isbn')#add to handle the isbn
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



@app.route('/sort_books')
def sort_books():
    """sorting"""
    sort_by = request.args.get('sort_by', 'title')

    #query and sort
    if sort_by == 'title':
        books = Book.query.order_by(Book.title).all()
    elif sort_by == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.all()

    books_with_covers = []

    for book in books:
        cover_url = 'static/default_image.jpg'

        books_with_covers.append({
            'id': book.id,
            'title': book.title,
            'author': book.author.name,
            'cover': cover_url
        })

    return render_template('home.html', books=books_with_covers, sort_by=sort_by)


@app.route('/search', methods=['GET'])
def search_books():
    """Search books by autor, title"""
    query = request.args.get('query', '').strip()

    if query:
        books = Book.query.join(Author).filter(
            (Book.title.ilike(f'%{query}%')) | (Author.name.ilike(f'%{query}%'))
        ).all()
    else:
        books = Book.query.all()

    books_with_covers = []
    for book in books:

        cover_url = 'static/default_image.jpg'
        books_with_covers.append({
            'id': book.id,
            'title': book.title,
            'author': book.author.name,
            'cover': cover_url
        })

    return render_template('home.html', books=books_with_covers)

@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """delete book by  book_id."""
    book = Book.query.get_or_404(book_id)
    author = book.author

    try:
        db.session.delete(book)
        db.session.commit()

        #condition to check the author
        if not Book.query.filter_by(author_id=author.id).first():
            # delete author also
            db.session.delete(author)
            db.session.commit()

        flash('Book deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting book: {e}', 'danger')

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
