from wtforms import form, fields


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

# Curriculum View form
# ClassItem Form
class CourseForm(form.Form):
    name = fields.StringField('name')
    description = fields.StringField('description')
    core = fields.StringField('core')
    
        
# Curriculum form
class CurriculumForm(form.Form):
    name = fields.StringField('curriculum')
    school = fields.SelectField('School', widget=Select2Widget())

    # Form list
    Course = InlineFieldList(InlineFormField(CourseForm))
    
class CurriculumView(ModelView):
    
    
    def is_accessible(self):
       
        
        return current_user.is_authenticated()
    
    column_list = ("name","schoolName")
    column_sortable_list = ('name')
    form = CurriculumForm
    
    
    def get_list(self, *args, **kwargs):
        count, data = super(CurriculumView, self).get_list(*args, **kwargs)

       
        for d in data:
            sid=d["school"]
            school=db.School.find_one({"_id":ObjectId(sid)})
            #print(school)
            
            d["schoolName"]=school["name"]

        return count, data
    
        # Contribute list of user choices to the forms
    def _feed_school_choices(self, form):
        school = db.School.find(fields=('name',))
        form.school.choices = [(str(x['_id']), x['name']) for x in school]
        return form

    def create_form(self):
        form = super(CurriculumView, self).create_form()
        return self._feed_school_choices(form)

    def edit_form(self, obj):
        form = super(CurriculumView, self).edit_form(obj)
        return self._feed_school_choices(form)
