""" 
Model for documents.
Copyright 2010 D. Robert Adams
"""

from google.appengine.ext import db

class DocumentModel(db.Model):
    author = db.UserProperty(auto_current_user_add=True)
    title = db.StringProperty()
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)