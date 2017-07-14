from flask import Flask
from flask_login import LoginManager
import flask_admin as admin
from .fadmin import UserView,TweetView,db




app = Flask(__name__)

app.config.from_object('config')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'



# Create admin
admin = admin.Admin(app, name='LearningBrix')

# Add views
admin.add_view(UserView(db.Users, 'Users'))
admin.add_view(TweetView(db.tweet, 'Tweet'))

from app import views

