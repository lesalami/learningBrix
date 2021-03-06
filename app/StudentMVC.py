

from wtforms import form, fields
from flask import  url_for, Markup

from flask_admin.contrib.pymongo import ModelView, filters
from flask_admin.model.fields import InlineFormField, InlineFieldList


from flask_login import current_user

from werkzeug.security import generate_password_hash
from flask_admin.form import Select2Widget, DatePickerWidget
from flask_admin.form import widgets
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId


db = MongoClient()["learningBrix"]


def getListOfClasses():
    classes = db.Classes.find(fields=('name',))
    choices = [(str(x['_id']), x['name']) for x in classes]
        
    return choices

# School form
class StudentForm(form.Form):
    fname = fields.StringField('fname')
    mname = fields.StringField('mname')
    lname = fields.StringField('lname')
    dob=fields.StringField('dob', widget=widgets.DatePickerWidget())
    school=fields.SelectField('School', widget=Select2Widget())
    classAssigned=fields.SelectField('classAssigned', widget=Select2Widget(), choices=getListOfClasses())



    
class StudentView(ModelView):
    def is_accessible(self):
       
        
        return current_user.is_authenticated()
    
    def user_link_formatter(view, context, model, name):
    
        id = model["_id"]
        url = "/admin/grades?sid="+str(id)
        name=model["fname"]
        return Markup('<a href="{}">{}</a>').format(url,name)
    
    
   
    
    column_details_list = ('fname','mname','lname', 'schoolName','dob','className')
    def user_link_formatter(view, context, model, name):
    
        id = model["_id"]
        url = "/admin/grades?sid="+str(id)
        name=model["fname"]
        return Markup('<a href="{}">{}</a>').format(url,name)
    
    
   
    
    column_details_list = ('fname','mname','lname', 'schoolName','dob','className')
    def user_link_formatter(view, context, model, name):
    
        id = model["_id"]
        url = "/admin/grades?sid="+str(id)
        name=model["fname"]
        return Markup('<a href="{}">{}</a>').format(url,name)
    
    
    def action_link_formatter(view, context, model, name):
    
        id = model["_id"]
        url = "/admin/grades?sid="+str(id)
        name=model["fname"]
        return Markup('<a href="{}">{}</a>').format(url,"Enter Grades")
    
    
   
    
    column_details_list = ('fname','mname','lname', 'schoolName','dob','className')
    column_list = ('fname','mname','lname', 'schoolName','dob','className','Action')
    column_formatters = {"fname": user_link_formatter,"Action":action_link_formatter}
    
    column_formatters = {"fname": user_link_formatter}
    
    column_formatters = {"fname": user_link_formatter}
    
    column_sortable_list = ('fname')
    column_searchable_list = ('fname', 'className')
    column_filters = (filters.FilterEqual('fname', 'fname'),
                       filters.FilterNotEqual('fname', 'fname'),
                       filters.FilterLike('fname', 'fname'),
                       filters.FilterEqual('className', 'className'),
                       filters.FilterLike('schoolName', 'schoolName'))
    form = StudentForm
    
    
    def get_list(self, *args, **kwargs):
        count, data = super(StudentView, self).get_list(*args, **kwargs)

       
        for d in data:
            sid=d["school"]
            school=db.School.find_one({"_id":ObjectId(sid)})
            cid=d["classAssigned"]
            classAssigned=db.Classes.find_one({"_id":ObjectId(cid)})
            #print(school)
            
            d["schoolName"]=school["name"]
            d["className"]=classAssigned["name"]
                
           

        

        return count, data

    
        # Contribute list of user choices to the forms
    def _feed_school_choices(self, form):
        school = db.School.find(fields=('name',))
        form.school.choices = [(str(x['_id']), x['name']) for x in school]
        return form

    def create_form(self):
        form = super(StudentView, self).create_form()
        return self._feed_school_choices(form)

    def edit_form(self, obj):
        form = super(StudentView, self).edit_form(obj)
        return self._feed_school_choices(form)
    