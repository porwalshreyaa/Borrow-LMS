from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_reads_book = db.Table('user_reads_book',
    db.Column('Book_id', db.Integer, db.ForeignKey('Books.Id')),
    db.Column('User_id', db.Integer, db.ForeignKey('Users.Id')),
    db.Column('status', db.String(), nullable=False, default='requested'),
    db.Column('issue', db.String(), nullable=True)
)
books_in_section = db.Table('books_in_section', 
    db.Column('Book_id', db.Integer, db.ForeignKey('Books.Id')),
    db.Column('Section_id', db.Integer, db.ForeignKey('Sections.Id')) 
)

class User(db.Model):
    __tablename__ = 'Users'
    _id = db.Column("Id", db.Integer, autoincrement=True, primary_key=True)
    password = db.Column("PassKey", db.String(512), nullable=False)
    username = db.Column("UserName", db.String(), unique=True, nullable=False)
    email = db.Column("Email", db.String(64), unique=True, nullable=False)
    role = db.Column("Role", db.String(8), nullable=False )
    access  = db.Column("Access", db.String(), nullable=False )
    read_books = db.relationship('Book', secondary = user_reads_book, back_populates='read_by')
    
class Book(db.Model):
    __tablename__ = 'Books'
    _id = db.Column("Id", db.Integer, autoincrement=True,primary_key=True)
    name = db.Column("Name", db.String(), nullable=False)
    content = db.Column("Content", db.String(), nullable=True)
    path = db.Column("Path", db.String(), nullable=False)
    cover = db.Column("Cover", db.String(), nullable=True)
    authors = db.Column("Authors", db.String, nullable=False)
    read_by =  db.relationship('User', secondary = user_reads_book, back_populates='read_books')
    section = db.relationship('Section', secondary=books_in_section, back_populates='books' )


class Section(db.Model):
    __tablename__ = 'Sections'
    _id = db.Column("Id", db.Integer, autoincrement=True, primary_key=True)
    name = db.Column("Name", db.String(), nullable=False)
    description = db.Column("Description", db.String(), nullable=True)
    dateCreated = db.Column("DateCreated", db.String(), nullable=False)
    books = db.relationship('Book', secondary=books_in_section,  back_populates='section')



