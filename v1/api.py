from flask import Flask,jsonify, request
from flask_restful import Api, Resource, reqparse

from model import *

from app import app
api = Api(app) 



# making a class for a particular resource 
# the get, post methods correspond to get and post requests 
# they are automatically mapped by flask_restful. 
# other methods include put, delete, etc. 

# Resource for CRUD operations
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return {
                    'id': user._id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'access': user.access,
                    'read_books': [book.name for book in user.read_books]  # Example: Include only book names
                }
            return {'message': 'User not found'}, 404
        else:
            users = User.query.all()
            return [{
                'id': user._id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'access': user.access,
                'read_books': [book.name for book in user.read_books]  # Example: Include only book names
            } for user in users]

    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('role', type=str, default="student", help='Role is required')
        parser.add_argument('access', type=str,  default=1, help='Access is required')
        args = parser.parse_args()
        
        new_user = User(username=args['username'], password=args['password'], 
                        email=args['email'], role=args['role'], access=args['access'])
        db.session.add(new_user)
        db.session.commit()
        
        return new_user.__dict__, 201
    
    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            parser.add_argument('password', type=str)
            parser.add_argument('email', type=str)
            parser.add_argument('role', type=str)
            parser.add_argument('access', type=str)
            args = parser.parse_args()
            
            for key, value in args.items():
                if value:
                    setattr(user, key, value)
            db.session.commit()
            
            return user.__dict__, 200
        return {'message': 'User not found'}, 404
    
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}
        return {'message': 'User not found'}, 404



class BookResource(Resource):
    def get(self, book_id=None):
        if book_id:
            book = Book.query.get(book_id)
            if book:
                return {
                    'id': book._id,
                    'name': book.name,
                    'content': book.content,
                    'path': book.path,
                    'cover': book.cover,
                    'authors': book.authors,
                    'section': [section.name for section in book.section] if book.section else None  # Example: Include section name
                }
            return {'message': 'Book not found'}, 404
        else:
            books = Book.query.all()
            return [{
                'id': book._id,
                'name': book.name,
                'content': book.content,
                'path': book.path,
                'cover': book.cover,
                'authors': book.authors,
                'section': [section.name for section in book.section] if book.section else None  # Example: Include section name
            } for book in books]
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('content', type=str)
        parser.add_argument('path', type=str, required=True, help='Path is required')
        parser.add_argument('cover', type=str)
        parser.add_argument('authors', type=str, required=True, help='Authors are required')
        args = parser.parse_args()
        
        new_book = Book(name=args['name'], content=args['content'], path=args['path'], 
                        cover=args['cover'], authors=args['authors'])
        db.session.add(new_book)
        db.session.commit()
        
        return new_book.__dict__, 201
    
    def put(self, book_id):
        book = Book.query.get(book_id)
        if book:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str)
            parser.add_argument('content', type=str)
            parser.add_argument('path', type=str)
            parser.add_argument('cover', type=str)
            parser.add_argument('authors', type=str)
            args = parser.parse_args()
            
            for key, value in args.items():
                if value:
                    setattr(book, key, value)
            db.session.commit()
            
            return book.__dict__, 200
        return {'message': 'Book not found'}, 404
    
    def delete(self, book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'message': 'Book deleted successfully'}
        return {'message': 'Book not found'}, 404

# Resource for Section CRUD operations
class SectionResource(Resource):
    def get(self, section_id=None):
        if section_id:
            section = Section.query.get(section_id)
            if section:
                return {
                    'id': section._id,
                    'name': section.name,
                    'description': section.description,
                    'dateCreated': section.dateCreated,
                    'books': [book.name for book in section.books] 
                }
            return {'message': 'Section not found'}, 404
        else:
            sections = Section.query.all()
            return [{
                'id': section._id,
                'name': section.name,
                'description': section.description,
                'dateCreated': section.dateCreated,
                'books': [book.name for book in section.books] 
            } for section in sections]
            
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('description', type=str)
        parser.add_argument('dateCreated', type=str, required=True, help='DateCreated is required')
        args = parser.parse_args()
        
        new_section = Section(name=args['name'], description=args['description'], dateCreated=args['dateCreated'])
        db.session.add(new_section)
        db.session.commit()
        
        return  {
                 'id': new_section._id,
                    'name': new_section.name,
                    'description': new_section.description,
                    'dateCreated': new_section.dateCreated,
                    'books': [book.name for book in new_section.books] 
                }, 201
    
    def put(self, section_id):
        section = Section.query.get(section_id)
        if section:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str)
            parser.add_argument('description', type=str)
            parser.add_argument('dateCreated', type=str)
            args = parser.parse_args()
            
            for key, value in args.items():
                if value:
                    setattr(section, key, value)
            db.session.commit()
            
            return {
                    'id': section._id,
                    'name': section.name,
                    'description': section.description,
                    'dateCreated': section.dateCreated,
                    'books': [book.name for book in section.books] 
                }, 200
        return {'message': 'Section not found'}, 404
    
    def delete(self, section_id):
        section = Section.query.get(section_id)
        if section:
            db.session.delete(section)
            db.session.commit()
            return {'message': 'Section deleted successfully'}
        return {'message': 'Section not found'}, 404




class BookAssignment(Resource):
    def post(self, book_id, section_id):
        book = Book.query.get(book_id)
        section = Section.query.get(section_id)
        if not book or not section:
            return {'message': 'Book or section not found'}, 404

        if book in section.books:
            return {'message': 'Book already assigned to section'}, 400

        section.books.append(book)
        db.session.commit()

        return {'message': 'Book assigned successfully'}, 201

    def delete(self, book_id, section_id):
        section = Section.query.get(section_id)
        book = Book.query.get(book_id)
        if book and section:
            if book in section.books:
                section.books.remove(book)
                db.session.commit()
                return {'message': f'Book {book_id} removed from section {section_id}'}, 200
            else:
                return {'message': f'Book {book_id} is not in section {section_id}'}, 404
        else:
            return {'message': 'Book or Section not found'}, 404

# Define routes

api.add_resource(UserResource, '/api/user', '/api/user/<int:user_id>')
api.add_resource(BookResource, '/api/book', '/api/book/<int:book_id>')
api.add_resource(SectionResource, '/api/section', '/api/section/<int:section_id>')
api.add_resource(BookAssignment, '/api/book/<int:book_id>/section/<int:section_id>')

