from flask import Flask
from model import db
from dotenv import load_dotenv
import os

from dotenv import load_dotenv
from os import getenv

current_dir= os.path.abspath(os.path.dirname(__file__))


api = None

# configuration
load_dotenv()

app = Flask(__name__)


# app.permanent_session_lifetime = timedelta(days=7)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir,"db.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
db.init_app(app)
with app.app_context():
    db.create_all()    
from routes import *

from model import *
# db.init_app(app)
# with app.app_context():
#     db.create_all()

###################### API Part ########################
from api import UserResource, BookResource, SectionResource
###################### API Part ########################



if __name__ == "__main__":
    app.run(debug=True)
