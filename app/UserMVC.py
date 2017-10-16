

from wtforms import form, fields

from .user import User
from flask_admin.contrib.pymongo import ModelView
from flask_admin.model.fields import InlineFormField, InlineFieldList


from flask_login import current_user

from werkzeug.security import generate_password_hash
from wtforms.validators import DataRequired,Email
from wtforms.validators import ValidationError
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

db = MongoClient()["learningBrix"]



def validate_email(form, field):
        
    Uzer=db.Users.find_one({"email":field.data})
    
    if Uzer:
        raise ValidationError('User already Exists')

class UserForm(form.Form):
    email = fields.StringField("email",validators=[DataRequired(),Email()])
    password = fields.PasswordField('password',validators=[DataRequired()])
    fname = fields.StringField('fname',validators=[DataRequired()])
    lname = fields.StringField('lname',validators=[DataRequired()])



class UserView(ModelView):
    def is_accessible(self):
        
        return current_user.is_authenticated() 

    column_list = ('fname','lname', 'email')
    column_sortable_list = ('fname', 'email')
    form = UserForm
    
    
    def edit_form(self, obj):
        
        form=ModelView.edit_form(self, obj)
        
        
        
        return form
    
    # Correct user_id reference before saving
    def on_model_change(self, form, model, is_created):
        password = model.get('password')
        model['password'] = generate_password_hash(password)
        
        if is_created:
            
            Uzer=db.Users.find_one({"email":model.get("email")})
       
            if Uzer:
                raise ValidationError('User already Exists')
            


        return model

    
    
