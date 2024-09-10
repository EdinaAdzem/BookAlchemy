from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#defining the author model class
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<Author {self.name}>'

    def __str__(self):
        return f'Author(name={self.name}, birth_date={self.birth_date}, date_of_death={self.date_of_death})'


#defining the book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        return f'<Book {self.title}>'

    def __str__(self):
        return f'Book(title={self.title}, author_id={self.author_id})'
