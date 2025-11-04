from flask_restful import Api
from app.resources.user_resource import UserResource
# from app.resources.book_resource import BookResource
# from app.resources.section_resource import SectionResource
# from app.resources.assignment_resource import BookAssignmentResource
from app.controllers.web_routes import web_bp

def register_routes(app):
    # Web routes (HTML)
    app.register_blueprint(web_bp)

    # REST API
    api = Api(app)
    api.add_resource(UserResource, '/api/users', '/api/users/<int:user_id>')
    # api.add_resource(BookResource, '/api/books', '/api/books/<int:book_id>')
    # api.add_resource(SectionResource, '/api/sections', '/api/sections/<int:section_id>')
    # api.add_resource(BookAssignmentResource, '/api/books/<int:book_id>/sections/<int:section_id>')
