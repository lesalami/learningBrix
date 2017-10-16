from wtforms import form, fields


from flask_admin.contrib.pymongo import ModelView, filters
from flask_admin.model.fields import InlineFormField, InlineFieldList
from flask import  url_for, Markup


from flask_login import current_user

from werkzeug.security import generate_password_hash
from flask_admin.form import Select2Widget, DatePickerWidget
from flask_admin.form import widgets
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId


db = MongoClient()["learningBrix"]

class ClassForm(form.Form):
    name = fields.StringField('name')
    curriculum = fields.SelectField('curriculum', widget=Select2Widget())
    school = fields.SelectField('school', widget=Select2Widget())
    order=fields.StringField('order')
    
class ClassView(ModelView):
    def is_accessible(self):
       
        
        return current_user.is_authenticated()
    
    
    def action_link_formatter(view, context, model, name):
    
        id = model["_id"]
        url = "/admin/classdetails?cid="+str(id)
        
        return Markup('<a href="{}">{}</a>').format(url,"View Students")
    
    column_list = ("name","schoolName","order","curriculumName","Action")
    column_sortable_list = ('name')
    column_formatters = {"Action":action_link_formatter}

    form = ClassForm
    
    def get_list(self, *args, **kwargs):
        count, data = super(ClassView, self).get_list(*args, **kwargs)

       
        for d in data:
            sid=d["school"]
            school=db.School.find_one({"_id":ObjectId(sid)})
            cid=d["curriculum"]
            curriculum=db.Curriculum.find_one({"_id":ObjectId(cid)})
            #print(school)
            
            d["schoolName"]=school["name"]
            d["curriculumName"]=curriculum["name"]

        return count, data
    
        # Contribute list of user choices to the forms
    def _feed_school_choices(self, form):
        school = db.School.find(fields=('name',))
        curriculum = db.Curriculum.find(fields=('name',))
        form.school.choices = [(str(x['_id']), x['name']) for x in school]
        form.curriculum.choices = [(str(x['_id']), x['name']) for x in curriculum]
        return form

    def create_form(self):
        form = super(ClassView, self).create_form()
        return self._feed_school_choices(form)

    def edit_form(self, obj):
        form = super(ClassView, self).edit_form(obj)
        return self._feed_school_choices(form)
