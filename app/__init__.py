from flask import Flask
from flask_login import LoginManager
import flask_admin as admin
from flask_admin import AdminIndexView,expose
from .fadmin import UserView,TweetView,SchoolView,StudentView,db




app = Flask(__name__)

app.config.from_object('config')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        userCount = db.Users.count()
        schoolObject = 'school object'
        return self.render('admin/index.html', userCount=userCount,schoolObject=schoolObject)

# Create admin
admin = admin.Admin(app, name='LearningBrix',index_view=MyHomeView())

# Add views
admin.add_view(UserView(db.Users, 'Users'))
admin.add_view(SchoolView(db.School, 'School'))
admin.add_view(StudentView(db.Students, 'Students'))

admin.add_view(TweetView(db.tweet, 'Tweet'))


from app import views

