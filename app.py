import os
from flask import Flask, render_template, request, redirect, url_for, flash
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


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        # Get data out of the form
        name = request.form['name']
        birth_date = request.form.get('birth_date')
        date_of_death = request.form.get('date_of_death')

        # auth obj
        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)

        try:
            # Add the new author to the database
            db.session.add(new_author)
            db.session.commit()
            flash('Author added successfully!', 'success')
            return redirect(url_for('add_author'))
        except Exception as e:
            db.session.rollback()  # roll back in case of issues like sevice down
            flash(f'Author could not be added, please check the services: {e}', 'danger')

    return render_template('add_author.html')

if __name__ == "__main__":
    app.run(debug=True)
