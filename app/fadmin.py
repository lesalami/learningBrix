import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

from flask import Flask
import flask_admin as admin


from wtforms import form, fields

from flask_admin.form import Select2Widget, DatePickerWidget
from flask_admin.contrib.pymongo import ModelView, filters
from flask_admin.model.fields import InlineFormField, InlineFieldList
from flask_admin import BaseView,expose
from .user import User
from flask import session, redirect,url_for,request
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.form import widgets
from flask_admin.form.widgets import DateTimePickerWidget
from werkzeug.security import generate_password_hash




# Create models
db = MongoClient()["learningBrix"]


# User admin
class InnerForm(form.Form):
    age = fields.StringField('age')
    dob = fields.StringField('dob')


class UserForm(form.Form):
    email = fields.StringField('email')
    password = fields.StringField('password')
    fname = fields.StringField('fname')
    lname = fields.StringField('lname')

    # Inner form
    inner = InlineFormField(InnerForm)

    # Form list
    form_list = InlineFieldList(InlineFormField(InnerForm))


class UserView(ModelView):
    def is_accessible(self):
        
        return current_user.is_authenticated() 

    column_list = ('fname','lname', 'email')
    column_sortable_list = ('fname', 'email')

    form = UserForm
    
    # Correct user_id reference before saving
    def on_model_change(self, form, model):
        password = model.get('password')
        model['password'] = generate_password_hash(password)

        return model
    


# Tweet view
class TweetForm(form.Form):
    name = fields.StringField('name')
    user_id = fields.SelectField('Users', widget=Select2Widget())
    text = fields.StringField('Text')

    testie = fields.BooleanField('Test')


class TweetView(ModelView):
    def is_accessible(self):
       
        
        return current_user.is_authenticated()
    
    column_list = ('name', 'user_id','text')
    column_sortable_list = ('fname')

    column_filters = (filters.FilterEqual('name', 'name'),
                      filters.FilterNotEqual('name', 'name'),
                      filters.FilterLike('name', 'name'),
                      filters.FilterNotLike('name', 'name'),
                      filters.BooleanEqualFilter('testie', 'Testie'))

    column_searchable_list = ('fname', 'text')

    form = TweetForm
    



    def get_list(self, *args, **kwargs):
        count, data = super(TweetView, self).get_list(*args, **kwargs)

        # Grab user names
        query = {'_id': {'$in': [x['user_id'] for x in data]}}
        users = db.users.find(query, fields=('fname',))

        # Contribute user names to the models
        users_map = dict((x['_id'], x['fname']) for x in users)

        for item in data:
            item['email'] = users_map.get(item['user_id'])

        return count, data

    # Contribute list of user choices to the forms
    def _feed_user_choices(self, form):
        users = db.Users.find(fields=('fname',))
        form.user_id.choices = [(str(x['_id']), x['fname']) for x in users]
        return form

    def create_form(self):
        form = super(TweetView, self).create_form()
        return self._feed_user_choices(form)

    def edit_form(self, obj):
        form = super(TweetView, self).edit_form(obj)
        return self._feed_user_choices(form)

    # Correct user_id reference before saving
    def on_model_change(self, form, model):
        user_id = model.get('user_id')
        model['user_id'] = ObjectId(user_id)

        return model
    



# Branch Form
class BranchForm(form.Form):
    branch = fields.StringField('branch')
    address = fields.StringField('address')
    
        
# School form
class SchoolForm(form.Form):
    name = fields.StringField('name')

    # Form list
    Branch = InlineFieldList(InlineFormField(BranchForm))
   
    
# School view        
class SchoolView(ModelView):
    def is_accessible(self):
       
        
        return current_user.is_authenticated()
    
    column_list = ('name', 'branchName')
    column_sortable_list = ('name')

    column_filters = (filters.FilterEqual('name', 'name'),filters.FilterNotEqual('name', 'name'),filters.FilterLike('name', 'name'),filters.FilterNotLike('name', 'name'))
                     

    column_searchable_list = ('name', 'name')

    form = SchoolForm

    def get_list(self, *args, **kwargs):
        count, data = super(SchoolView, self).get_list(*args, **kwargs)

        # Grab user names
        #query = {'name': {'$in': [x['user_id'] for x in data]}}
       
        for d in data:
            bn=[]
            for b in d["Branch"]:
                bn.append(b["branch"])
            d["branchName"]=bn
                
           

        

        return count, data


# School form
class StudentForm(form.Form):
    fname = fields.StringField('fname')
    mname = fields.StringField('mname')
    lname = fields.StringField('lname')
    dob=fields.StringField('dob', widget=widgets.DatePickerWidget())
    school=fields.SelectField('School', widget=Select2Widget())
    
class StudentView(ModelView):
    def is_accessible(self):
       
        
        return current_user.is_authenticated()
    
    column_list = ('fname','mname','lname', 'schoolName','branchName')
    column_sortable_list = ('fname')
    form = StudentForm
    
    
    def get_list(self, *args, **kwargs):
        count, data = super(StudentView, self).get_list(*args, **kwargs)

       
        for d in data:
            sid=d["school"]
            school=db.School.find_one({"_id":ObjectId(sid)})
            print(school)
            
            d["schoolName"]=school["name"]
                
           

        

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
