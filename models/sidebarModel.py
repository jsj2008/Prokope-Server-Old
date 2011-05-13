""" 
Model for sidebar information.
Copyright 2011 D. Robert Adams
"""

from google.appengine.ext import db
from documentModel import DocumentModel

class SidebarModel(db.Model):
    author = db.UserProperty(auto_current_user_add=True)# who created this sidebar
    content = db.TextProperty()                         # sidebar text
    date = db.DateTimeProperty(auto_now_add=True)       # when created
    document = db.ReferenceProperty(DocumentModel)      # the document to which this sidebar refers
