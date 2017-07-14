import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

from flask import Flask
import flask_admin as admin


from wtforms import form, fields

from flask_admin.form import Select2Widget
from flask_admin.contrib.pymongo import ModelView, filters
from flask_admin.model.fields import InlineFormField, InlineFieldList
from flask_admin import BaseView,expose
from .user import User
from flask import session, redirect,url_for,request
from flask_login import current_user



# Create models
db = MongoClient()["learningBrix"]

class MyView(BaseView):
    def is_accessible(self):
        return False

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

    column_list = ('fname','lname', 'email', 'password')
    column_sortable_list = ('fname', 'email', 'password')

    form = UserForm


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


# Flask views
#@app.route('/')
#def index():
    #return '<a href="/admin/">Click me to get to Admin!</a>'


#if __name__ == '__main__':
    # Create admin
    #admin = admin.Admin(app, name='Example: PyMongo')

    # Add views
    #admin.add_view(UserView(db.user, 'User'))
    #admin.add_view(TweetView(db.tweet, 'Tweets'))

    # Start app
    #app.run(debug=True)