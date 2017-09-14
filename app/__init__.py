from flask import Flask
from flask_login import LoginManager
import flask_admin as admin
from flask_admin import AdminIndexView,expose
from .fadmin import UserView,SchoolView,StudentView,db,ClassView,CurriculumView,BaseView

from flask import request, flash, jsonify

from bson.objectid import ObjectId


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
    
    
class EnterGrades(BaseView):
    
   
    @expose('/')
    def index(self):
         
        sid = request.args.get('sid')
        schoolObject=None
        studentObject=None
        classes=None
        
        if(sid is not None):
            schoolObject = db.School.find() 
            studentObject=db.Students.find_one({"_id":ObjectId(sid)})
            classes=db.Classes.find({"school":studentObject["school"]})
        
        else:
            flash("No student record available", category='error')
         
       
        return self.render('admin/enterGrades.html',schoolObject=schoolObject, sid=sid, classes=classes)
    
    
    @app.route('/getCourses')
    def getCourses():
        selectedClass = request.args.get('selectedClass')
        
        
        print( selectedClass)
        
        curriculum_id=db.Classes.find_one({"_id":ObjectId(selectedClass)})
        print(curriculum_id["_id"])
        
        curriculum=db.Curriculum.find_one({"_id":ObjectId(selectedClass)})
        
        
        
        return jsonify(curriculum)

# Create admin
admin = admin.Admin(app, name='LearningBrix',index_view=MyHomeView())

# Add views
admin.add_view(UserView(db.Users, 'Users'))
#admin.add_view(SchoolView(db.School, 'School'))
admin.add_view(SchoolView(db.School, name="Schools",category="School"))
#admin.add_view(ClassGroupView(db.ClassGroup, name="Class Groups", category="School"))
admin.add_view(ClassView(db.Classes, name="Classes", category="School"))
admin.add_view(CurriculumView(db.Curriculum, name="Curriculum",category="School"))

admin.add_view(StudentView(db.Students, 'Students'))

admin.add_view(EnterGrades(name="Enter Grades",endpoint="grades",category="Grades"))

#admin.add_view(TweetView(db.tweet, 'Tweet'))


from app import views

