

from wtforms import form, fields


from flask_admin.contrib.pymongo import ModelView, filters
from flask_admin.model.fields import InlineFormField, InlineFieldList


from flask_login import current_user

from werkzeug.security import generate_password_hash


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
