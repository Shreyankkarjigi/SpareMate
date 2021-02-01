from flask import Flask,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES,UploadSet,configure_uploads,patch_request_class
from datetime import timedelta

from flask_login import LoginManager, login_required, login_user, logout_user


import os

basedir=os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = 'eeeopopdopeppokakopkoapkaopap'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///localhost24.db'
db = SQLAlchemy(app)
app.config['UPLOADED_PHOTOS_DEST']=os.path.join(basedir,'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app,photos)
patch_request_class(app) 

db = SQLAlchemy(app)
brcypt=Bcrypt(app)
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
from shop.admin import routes

from shop.products import routes