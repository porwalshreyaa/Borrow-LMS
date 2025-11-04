from flask_restful import Resource, reqparse
from app.models.user import User
from app.extensions import db
import re

USERNAME_REGEX = r'^[A-Za-z0-9_]{3,30}$'
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
ALLOWED_ROLES = {"student", "librarian"}


class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404
            
            return user.to_dict(), 200
        return [u.to_dict() for u in User.query.all()], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('role', type=str, choices=('student', 'teacher'), default='student', help='Role must be one of: student, teacher, admin')
        args = parser.parse_args()
        
        username = args['username'].strip()
        email = args['email'].strip().lower()
        role = args['role'].strip().lower()

        if not re.match(USERNAME_REGEX, username):
            return {"message": "Invalid username. Use 3-30 characters: letters, numbers, or underscores only."}, 400

        if not re.match(EMAIL_REGEX, email):
            return {"message": "Invalid email format."}, 400
        if len(email) > 255:
            return {"message": "Email too long."}, 413

        if role not in ALLOWED_ROLES:
            return {"message": f"Invalid role. Allowed roles: {', '.join(ALLOWED_ROLES)}"}, 400

        if User.query.filter_by(email=args['email']).first():
            return {"message": "Email already exists"}, 409
        elif User.query.filter_by(username=args['username']).first():
            return {"message": "Username occupied"}, 409
        user = User(**args)
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201
