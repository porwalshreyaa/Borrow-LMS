from flask import Flask, redirect, url_for, render_template, request, session, flash, abort
from app import app
from functools import wraps
import requests
from flask import jsonify
import json

from datetime import datetime, timedelta
from pytz import timezone

# from dotenv import load_dotenv
from os import getenv
import os

from werkzeug.utils import secure_filename
from model import User, Book, Section
from model import *
from model import db as db
# from application.model import db as db

from sqlalchemy import desc




def log_req(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return inner

def admin_req(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for("librarian"))
        return func(*args, **kwargs)
    return inner


@app.errorhandler(404)
def errorhandler(error):
    return render_template('index/404.html'), 404


def ref_books(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'username' in session:
            user_id
            return redirect(url_for("librarian"))
        return func(*args, **kwargs)
    return inner



def revoke_access():
    issued_books = db.session.query(user_reads_book).filter_by(status='issued').all()

    for issued_book in issued_books:
        issue_date = datetime.strptime(issued_book[3], '%Y-%m-%d %H:%M:%S.%f')

        if issue_date + timedelta(days=5) <= datetime.now():
            user_id = issued_book[1]
            book_id = issued_book[0]
            update = user_reads_book.update() \
                .where(user_reads_book.c.User_id == user_id) \
                .where(user_reads_book.c.Book_id == book_id) \
                .values(status='read')
            
            db.session.execute(update)
            db.session.commit()
            



#### admin---------------




@app.route("/admin/", methods = ['GET', 'POST'])
@admin_req
def admin():
    sections = Section.query.order_by(db.func.datetime(Section.dateCreated).desc()).all()
    if request.method == 'POST':
        content = request.form
        title = content.get('name')
        description = content.get('description')
        current = datetime.today().date()
        section = Section(name=title, description=description, dateCreated= current)
        db.session.add(section)
        db.session.commit()
        flash('Section Created!')
        return redirect(url_for('admin'))
    return render_template('admin/admin_home.html', sections= sections)
    

@app.route("/librarian", methods=['GET','POST'])
def librarian():
    if 'admin' in session:
        return redirect(url_for("admin"))
    if request.method == "POST":
        content = request.form
        username = content.get("username")
        password = content.get("password")
        user = User.query.filter_by(username=username, password=password).first()
        if user and user.role == 'librarian':
            session["admin"] = content.get("username")
            return redirect(url_for("admin"))

        else:
            flash("Invalid Credentials!")
            return redirect(url_for("librarian"))
            
    return render_template('librarian.html')



@app.route('/section/<int:section_id>', methods=['GET','POST'])
def section(section_id):
    section_id = int(section_id)
    section = Section.query.filter_by(_id = section_id).first()
    
    if request.method == 'POST':
        try:
            current_dir = os.getcwd()
            result = request.form
            title = result.get('title')
            author = result.get("author")
            description = result.get('description')
            if title and author:
                cover = request.files.get('cover')
                book_file = request.files.get("book")
                if cover and book_file:
                    if cover.filename == '' or book_file.filename == '':
                        flash('No selected file')
                        return redirect(url_for('enter'))
                    print(result)
                    cover_filename = secure_filename(cover.filename)
                    book_filename = secure_filename(book_file.filename)
                    print(cover_filename)
                    print(book_filename)
                    book_path = (os.path.join(current_dir,'static/pdfs/', book_filename))
                    cover_path = (os.path.join(current_dir,'static/images/', cover_filename))
                    print(book_path)
                    print(cover_path)
                    book_file.save(book_path)
                    cover.save(cover_path)
                    book = Book(name=title, content=description, path=book_filename, cover=cover_filename, authors=author)
                    section.books.append(book)
                    db.session.add(book)
                    db.session.commit()
                    return redirect(url_for('section', section_id=section_id))
                elif book_file:
                    flash('Please Upload coveri fle')
                    return redirect(url_for('enter'))
                elif cover:
                    flash('Please upload Book Pdf')
                else:
                    flash('Something is missing')
                    return redirect(url_for('enter'))
            else:
                flash('Title or Author Name is missing')
                return redirect(url_for('enter'))
        except:
            flash('No Pdf Uploaded!')
            return redirect(url_for('enter'))
    if section:
        books = section.books
        return render_template('lib/section.html', section= section, books=books)
    else:
        return 'Not Found', 404

@app.route('/edit_section/<int:section_id>', methods=['GET', 'POST'])
@admin_req
def edit_section(section_id):
    if request.method == 'POST':
        content = request.form
        title = content.get('name')
        description = content.get('description')
        section = Section.query.filter_by(_id=section_id).first()
        try:
            if section is None:
                flash('Section not found')
                return redirect(url_for('section', section_id=section_id))
            if title:
                section.name = title
                section.description=description
            db.session.commit()
            flash('Section Updated!')
            return redirect(url_for('section', section_id=section_id))
        except:
            flash('Error!')
            return redirect(url_for('section', section_id=section_id))
    


    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        try:
            # Update book attributes with form data
            if title:
                book.name = title
            if author:
                book.authors = author
            if description:
                book.content = description

            # Commit the changes to the database
            db.session.commit()
            flash('Book updated successfully!')
            return redirect(url_for('book', book_id=book_id))

        except:
            # db.session.rollback()
            flash('Error updating the book')    
            return redirect(url_for('book', book_id=book_id))

    return redirect(url_for('book', book_id=book_id))

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@admin_req
def edit_book(book_id):
    book = Book.query.filter_by(_id=book_id).first()
    if book is None:
        flash('Book not found')
        return redirect(url_for('book', book_id=book_id))

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        try:
            # Update book attributes with form data
            if title:
                book.name = title
            if author:
                book.authors = author
            if description:
                book.content = description

            # Commit the changes to the database
            db.session.commit()
            flash('Book updated successfully!')
            return redirect(url_for('book', book_id=book_id))

        except:
            # db.session.rollback()
            flash('Error updating the book')    
            return redirect(url_for('book', book_id=book_id))

    return redirect(url_for('book', book_id=book_id))

@app.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    book = Book.query.get(book_id)  # Retrieve the book to delete

    try:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!')
        return redirect(url_for('enter'))  

    except:
        db.session.rollback()
        flash('Error deleting the book' )
        return redirect(url_for('book', book_id=book_id))

    return redirect(url_for('book', book_id=book_id))
@app.route('/delete_section/<int:section_id>', methods=['GET', 'POST'])
def delete_section(section_id):
    section = Section.query.get(section_id)  # Retrieve the book to delete

    try:
        db.session.delete(section)
        db.session.commit()
        flash('Section deleted successfully!')
        return redirect(url_for('enter'))  

    except:
        db.session.rollback()
        flash('Error deleting the Section' )
        return redirect(url_for('section', section_id=section_id))

    return redirect(url_for('section', section_id=section_id))

@admin_req
@app.route('/requests')
def requests():
    requests = db.session.query(user_reads_book).filter_by(status= 'requested').all()
    return render_template('admin/requests.html',requests=requests)

@admin_req
@app.route('/issued')
def issued():
    issues = db.session.query(user_reads_book).filter_by(status= 'issued').all()
    return render_template('admin/granted.html',requests=issues)

@app.route('/grant/<int:user_id>/<int:book_id>')
def grant(user_id,book_id):
    user = User.query.get(user_id)
    book = Book.query.get(book_id)


    if not user:
        return jsonify({'error': 'User not found'}), 404
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    update = user_reads_book.update() \
    .where(user_reads_book.c.User_id == user._id) \
    .where(user_reads_book.c.Book_id == book_id) \
    .values(status='issued', issue=datetime.now())
    db.session.execute(update)
    db.session.commit()
    return redirect(url_for('issued'))


@app.route('/deny/<int:user_id>/<int:book_id>')
def deny(user_id,book_id):
    
    user = User.query.get(user_id)
    book = Book.query.get(book_id)


    if not user:
        return jsonify({'error': 'User not found'}), 404
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    delete_query = user_reads_book.delete() \
        .where(user_reads_book.c.User_id == user_id) \
        .where(user_reads_book.c.Book_id == book_id)
    db.session.execute(delete_query)
    db.session.commit()

    return redirect(url_for('enter'))

@app.route('/revoke/<int:user_id>/<int:book_id>')
def revoke(user_id,book_id):
    
    user = User.query.get(user_id)
    book = Book.query.get(book_id)


    if not user:
        return jsonify({'error': 'User not found'}), 404
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    update = user_reads_book.update() \
    .where(user_reads_book.c.User_id == user._id) \
    .where(user_reads_book.c.Book_id == book_id) \
    .values(status='read')
    db.session.execute(update)
    db.session.commit()

    return redirect(url_for('enter'))

# @app.route('/delete/<str:object>/<int:value>')
# @admin_req
# def delete(object, value):
#     if object == 'section':







@admin_req
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('admin/users_data.html',users=users)

@admin_req
@app.route('/admin/stats')
def lib_stats():
    pass


## common------------
@app.route("/")
def enter():
    if 'admin' in session:
        return redirect(url_for('admin'))
    return redirect(url_for('home'))
    

@app.route('/book/<int:book_id>')
def book(book_id):
    revoke_access()
    book_id = int(book_id)
    book = Book.query.get(book_id)
    if 'admin' in session:
        role = 'admin'
        return render_template('lib/book.html', book=book, role=role)
    if 'username' in session:
        usr = User.query.filter_by(username=session['username']).first()
        if book:
            user_book = db.session.query(user_reads_book).filter_by(User_id=usr._id, Book_id=book_id).first()
                
            if user_book:
                book_status = user_book.status
                return render_template('lib/book.html', book=book, status = book_status)
            return render_template('lib/book.html', book=book)
        else:
            flash('No such book found in the database')
            return redirect(url_for('enter'))
    return redirect(url_for('enter'))


# ########### user functionality

@app.route("/home")
@log_req
def home():
    
    user = User.query.filter_by(username = session['username']).first()
    sections = Section.query.order_by(db.func.datetime(Section.dateCreated).desc()).all()
    return render_template('lib/home.html', sections = sections, user=user) 

@app.route("/login", methods = [ 'GET','Post'])
def login():

    if 'username' in session:
        redirect(url_for("home"))
    elif request.method == "POST":
        content = request.form
        username = content.get("username")
        password = content.get("password")
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["username"] = content.get("username")
            print(session['username'])
            return redirect(url_for("home"))
        else:
            flash("Invalid Credentials!")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username', None)
        
    elif 'admin' in session:
        session.pop('admin', None)
    
    return redirect(url_for('home'))


@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        username = result["username"]
        password = result["password"]

        if User.query.filter_by(email=email).first():
            flash("User already exists!")
            return redirect(url_for("register"))
        elif User.query.filter_by(username=username).first():
            flash("Username occupied!")
            return redirect(url_for("register"))
        else:
            user = User(username= username, email=email, password= password, role='student', access=1)
            db.session.add(user)
            db.session.commit()
            
            flash('Congratulations!')
            flash('You can Log in!')
            return redirect(url_for("login"))
    return render_template('login.html')



@app.route("/search", methods=["GET", "POST"])
def search():
    books = Book.query.all()
    users = User.query.all()
    sections = Section.query.all()
    user = User.query.filter_by(username=session['username']).first()
    if request.method =='POST':
        form = request.form
        search_query = form.get("search_query")
        book_results = Book.query.filter(Book.name.ilike(f"%{search_query}%"))
        section_results = Section.query.filter(Section.name.ilike(f"%{search_query}%"))
        if book_results or section_results:
            return render_template("search.html", user=user, book_results=book_results,section_results=section_results)
    return redirect(url_for("enter"))



@app.route('/mybooks')
@log_req
def mybooks():
    
    username = session['username']
    user = User.query.filter_by(username = username).first()
    issued = db.session.query(user_reads_book).filter_by(status='issued', User_id=user._id).all()
    revoke_access()
    read = db.session.query(user_reads_book).filter_by(status='read', User_id=user._id).all()
    read_books = [Book.query.filter_by(_id = i[0]).first() for i in read]
    current_books = [Book.query.filter_by(_id = i[0]).first() for i in issued]

    return render_template('lib/mybooks.html',read_books=read_books, current_books=current_books)


@app.route("/profile")
@log_req
def profile():
    app.logger.debug("This is profile page")
    return render_template('index/var_content.html') 


@app.route('/return/book/<int:book_id>')
def return_book(book_id):
    book_id = int(book_id)
    book = Book.query.get(book_id)
    
    if 'admin' in session:
        return redirect(url_for('enter'))
    
    if 'username' in session:
        usr = User.query.filter_by(username=session['username']).first()
        
        if book:
            # Query the user's association with the book
            user_book = db.session.query(user_reads_book).filter_by(User_id=usr._id, Book_id=book_id).first()
            
            if user_book:
                # Update the status of the book
                if user_book.status == 'issued':
                    update = user_reads_book.update().where(user_reads_book.c.User_id == usr._id).where(user_reads_book.c.Book_id == book_id).values(status='read')
                    db.session.execute(update)
                    db.session.commit()
                    flash('Book returned successfully')
                else:
                    flash('Book is not currently issued')
            else:
                flash('You have not requested this book')
        else:
            flash('No such book found in the database')
    
    return redirect(url_for('enter'))

@app.route('/request/book/<int:book_id>')
def request_book(book_id):
    book_id = int(book_id)
    book = Book.query.get(book_id)
    user = User.query.filter_by(username=session['username']).first()
    user_id = user._id

    user_issued_books = db.session.query(user_reads_book).filter_by(User_id=user_id, status='issued').all()
    past_book = db.session.query(user_reads_book).filter_by(User_id=user_id, Book_id=book_id).first()

    if past_book:
        if past_book[2] == 'issued':
            flash('You have this book')

            return redirect(url_for('enter'))
        else:
            update = user_reads_book.update() \
                .where(user_reads_book.c.User_id == user_id) \
                .where(user_reads_book.c.Book_id == book_id) \
                .values(status='requested', issue='')
            db.session.execute(update)
            db.session.commit()
            return redirect(url_for('enter'))


    if user_issued_books and len(user_issued_books)>= 5:
        flash('You have reached your limit!')
        return redirect(url_for('enter'))
    if 'admin' in session:
        return redirect(url_for('enter'))
    
    if 'username' in session:
        usr = User.query.filter_by(username=session['username']).first()
        
        if book:
            # Query the user's association with the book
            if user_issued_books:
                for user_issued_book in user_issued_books:
                    if user_issued_books[0] == book_id:
                        flash('You already have this book')
                        return redirect(url_for('enter'))
            else:
                usr.read_books.append(book)
                db.session.commit()
                flash('Request Made!')
        else:
            flash('No such book found in the database')
    
    return redirect(url_for('enter'))

