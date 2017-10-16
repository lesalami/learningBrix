from flask import Flask
from flask_login import LoginManager
import flask_admin as admin
from flask_admin import AdminIndexView,expose
from .fadmin import UserView,SchoolView,StudentView,db,ClassView,CurriculumView,BaseView

from flask import request, flash, jsonify,json

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
    


class ClassDetails(BaseView):
    
    
    @expose('/')
    def index(self):
        
        cid = request.args.get('cid')
        schoolObject=None
        studentObject=None
        classes=None
        
        
        
        if(cid is not None):
            
            
            studentObject=db.Students.find({"classAssigned":cid})
            classObject=db.Classes.find_one({"_id":ObjectId(cid)})
            
            
        else:
            
            flash("No Class record available", category='error')            
                   
         
       
        return self.render('admin/classdetail.html', studentObject=studentObject, classObject=classObject)
        
    
    
    
    
class EnterGrades(BaseView):
    
    def is_visible(self):
        
        
        return False
    
   
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
        student_id=request.args.get('student_id')
        
        print( selectedClass)
        
        class_object=db.Classes.find_one({"_id":ObjectId(selectedClass)})
        
        curriculumID=class_object["curriculum"];
        
        print(curriculumID)
        
        curriculum=db.Curriculum.find_one({"_id":ObjectId(curriculumID)})
        coursesFound=curriculum["Course"]
        
        
        grades_object=db.Grades.find_one({
            "student_id":ObjectId(student_id),
             "school_id":ObjectId(curriculum["school"]), 
             "curriculum_id":ObjectId(curriculum["_id"]),
             "class_id":ObjectId(selectedClass)
             
             })
        
        dictPopulatedGrades={}
        
        if(grades_object):
            gradesEntry=grades_object["grades"]
            
            for course in coursesFound:
                for incomingGrade in gradesEntry:
                    if(course["name"]==incomingGrade["key"]):
                        course["value"]=incomingGrade["value"]
            
        
        #json=jsonify(coursesFound)
        
        print(coursesFound)
        
        response=json.dumps({'status':'ok','courses':coursesFound,'class_id':str(selectedClass),'school_id':str(curriculum["school"]),'curriculum_id':str(curriculum["_id"])})
        
        return response
    
    
    
    
    @app.route('/saveGrades', methods=['GET', 'POST'])
    def saveGrades():
        data = request.data
        dataDict = json.loads(data)
        gradedCourses = dataDict[0]['gradedCourses']
        school_id = dataDict[0]['school_id']
        class_id = dataDict[0]['class_id']
        student_id = dataDict[0]['student_id']
        curriculum_id = dataDict[0]['curriculum_id']
        
        

        
        grades_object=db.Grades.find_one({
            "student_id":ObjectId(student_id),
             "school_id":ObjectId(school_id), 
             "curriculum_id":ObjectId(curriculum_id),
             "class_id":ObjectId(class_id)
             
             })
        
        if(grades_object):                
            db.Grades.update({
                "student_id":ObjectId(student_id),
                "school_id":ObjectId(school_id), 
                "curriculum_id":ObjectId(curriculum_id)
                },{'$set':{"grades":gradedCourses}})
                         
                         
             
                 
             
        else:    
            doc={
            "student_id":ObjectId(student_id),
             "school_id":ObjectId(school_id),
             "curriculum_id":ObjectId(curriculum_id),
             "class_id":ObjectId(class_id),
             "grades":gradedCourses
    
             
             }
            
            db.Grades.save(doc)
        
        response=json.dumps({'status':'ok'})
        
        return response
        
        
        

# Create admin
admin = admin.Admin(app, name='LearningBrix',index_view=MyHomeView())

# Add views
admin.add_view(UserView(db.Users, 'Users'))
#admin.add_view(SchoolView(db.School, 'School'))
admin.add_view(SchoolView(db.School, name="Schools",category="School"))
#admin.add_view(ClassGroupView(db.ClassGroup, name="Class Groups", category="School"))
admin.add_view(ClassView(db.Classes, name="Classes", category="School"))

admin.add_view(CurriculumView(db.Curriculum, name="Curriculum", category="School"))

admin.add_view(ClassDetails(name="Class Details",category="School"))

admin.add_view(StudentView(db.Students, 'Students and Grades'))

admin.add_view(EnterGrades(name="Enter Grades",endpoint="grades",category="Grades"))

#admin.add_view(TweetView(db.tweet, 'Tweet'))


from app import views

