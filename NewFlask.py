from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


# SQLAlchemy stuff

app.config.update(

    SECRET_KEY='asdf4809uasd908r3q450a987fsdf9043j6l23io6u2nhvgbpo932u5gasdf2q345bhwqe',
    # SQLALCHEMY_DATABASE_URI='<database>://<user_id>:<password>@<server>/<database_name>',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:password@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)


db = SQLAlchemy(app)






@app.route('/')  # called a decorator
def hello_world():
    return 'Hello World!'

#JINJA TEMPLATES
@app.route('/watch')
def top_movies():
    movie_list = ['autopsy of jane doe',
                  'neon demon',
                  'ghost in a shell',
                  'kong: skull island',
                  'john wick 2',
                  'spiderman - homecoming']

    return render_template('movies.html',
                           movies=movie_list,
                           name='Harry')


@app.route('/tables')
def movies_plus():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.48}

    return render_template('table_data.html',
                           movies=movies_dict,
                           name="Sally")


@app.route('/filters')
def filter_data():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.48}

    return render_template('filter_data.html',
                           movies=movies_dict,
                           name=None,
                           film='a christmas carol')


@app.route('/macros')
def jinja_macros():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.48}

    return render_template('using_macros.html',
                           movies=movies_dict)


# SQLAlchemy database class/methods

# Tables are creating by making a new class of type db.Model

# A db.Model object is a new Table
class Publication(db.Model):
    __tablename__ = 'publication'

    # One of the benefits of SQLAlchemy is we can create tables here in Python, rather than writing SQL in the database platform
    # The ORM (Object Relational Mapper) converts the class definitions to the SQL statements

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    # in-built python methods
    # __init__() is called when new instances of a class are created, it initializes reference variables and attributes
    # __repr__() takes only 1 parameter, self, and returns a string representation of an instance,
    #                this helps in formatting and producing a readble output of the data

    def __init__(self, name):

        self.name = name

    def __repr__(self):
        return 'Publisher is {}'.format(self.name)




# A db.Model object is a new Table
class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    # The index=True attribute will speed up retrieving records from the database
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    # String it not the image itself, but the filepath to the image
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    # this datetime is from the Python library (and not SQLAlchemy) and needs to be imported above
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())


    # Relationship - this establishes the relationship from this 'book' table to the 'publication' table above
    # It sets the book's 'pub_id' value as a Foreign Key to the publication table's 'id' values
    # Each Publisher in the publication table contains unique books from that publisher alone

    # This is a 1-to-Many relationship between the publication.id and the book.pub_id
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):

        # book_id and pub_date have been left out because they are automatically generated and can't be changed
        # they will render on their own in the table
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return 'The title is {} by author {}'.format(self.title, self.author)


if __name__ == '__main__':

    # SQLAlchemy line to initialize the all the tables in the database, but only if they don't already exist
    # if the tables are already up and running then this line is skipped
    db.create_all()

    app.run(debug=True)