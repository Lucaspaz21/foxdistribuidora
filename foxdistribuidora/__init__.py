from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = 'c8adf5def159745c130e889bb6359899'

if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fox.db'

database = SQLAlchemy(app)

from foxdistribuidora import routes
