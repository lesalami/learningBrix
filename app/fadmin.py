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
from flask import session, redirect,url_for,request
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.form import widgets
from flask_admin.form.widgets import DateTimePickerWidget
from werkzeug.security import generate_password_hash




# Create models
db = MongoClient()["learningBrix"]


from .UserMVC import UserForm,UserView

from .SchoolMVC import *

from .StudentMVC import *

from .ClassMVC import *

from .CurriculumMVC import *


# Tweet view
# class TweetForm(form.Form):
#     name = fields.StringField('name')
#     user_id = fields.SelectField('Users', widget=Select2Widget())
#     text = fields.StringField('Text')
# 
#     testie = fields.BooleanField('Test')


# class TweetView(ModelView):
#     def is_accessible(self):
#        
#         
#         return current_user.is_authenticated()
#     
#     column_list = ('name', 'user_id','text')
#     column_sortable_list = ('fname')
# 
#     column_filters = (filters.FilterEqual('name', 'name'),
#                       filters.FilterNotEqual('name', 'name'),
#                       filters.FilterLike('name', 'name'),
#                       filters.FilterNotLike('name', 'name'),
#                       filters.BooleanEqualFilter('testie', 'Testie'))
# 
#     column_searchable_list = ('fname', 'text')
# 
#     form = TweetForm
#     
# 
# 
# 
#     def get_list(self, *args, **kwargs):
#         count, data = super(TweetView, self).get_list(*args, **kwargs)
# 
#         # Grab user names
#         query = {'_id': {'$in': [x['user_id'] for x in data]}}
#         users = db.users.find(query, fields=('fname',))
# 
#         # Contribute user names to the models
#         users_map = dict((x['_id'], x['fname']) for x in users)
# 
#         for item in data:
#             item['email'] = users_map.get(item['user_id'])
# 
#         return count, data
# 
#     # Contribute list of user choices to the forms
#     def _feed_user_choices(self, form):
#         users = db.Users.find(fields=('fname',))
#         form.user_id.choices = [(str(x['_id']), x['fname']) for x in users]
#         return form
# 
#     def create_form(self):
#         form = super(TweetView, self).create_form()
#         return self._feed_user_choices(form)
# 
#     def edit_form(self, obj):
#         form = super(TweetView, self).edit_form(obj)
#         return self._feed_user_choices(form)
# 
#     # Correct user_id reference before saving
#     def on_model_change(self, form, model):
#         user_id = model.get('user_id')
#         model['user_id'] = ObjectId(user_id)
# 
#         return model
    






    
    

    

    
    
    
    
    
    
    





# Class View form
# ClassItem Form

# def getCurriculums():
#     curriculum = db.Curriculum.find(fields=('name',))
#     choices = [(str(x['_id']), x['name']) for x in curriculum]
#         
#     return choices
#     
#   
#        
# #classGroupForm form
# class ClassGroupForm(form.Form):
#     name = fields.StringField('classGroup')
#     school = fields.SelectField('School', widget=Select2Widget())
# 
# 
#     
# class ClassGroupView(ModelView):
#     def is_accessible(self):
#        
#         
#         return current_user.is_authenticated()
#     
#     column_list = ("name","schoolName")
#     column_sortable_list = ('name')
#     form = ClassGroupForm
#     
#     
#     def get_list(self, *args, **kwargs):
#         count, data = super(ClassGroupView, self).get_list(*args, **kwargs)
# 
#        
#         for d in data:
#             sid=d["school"]
#             school=db.School.find_one({"_id":ObjectId(sid)})
#             #print(school)
#             
#             d["schoolName"]=school["name"]
# 
#         return count, data
#     
#         # Contribute list of school and curriculum choices to the forms
#     def _feed_school_choices(self, form):
#         school = db.School.find(fields=('name',))
#         form.school.choices = [(str(x['_id']), x['name']) for x in school]
#         #curriculum = db.Curriculum.find(fields=('name',))
#         #form.Class.InlineFormField.form.curriculum.choices = [(str(x['_id']), x['name']) for x in curriculum]
#         return form
# 
#     def create_form(self):
#         form = super(ClassGroupView, self).create_form()
#         return self._feed_school_choices(form)
# 
#     def edit_form(self, obj):
#         form = super(ClassGroupView, self).edit_form(obj)
#         return self._feed_school_choices(form)

