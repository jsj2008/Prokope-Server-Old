""" 
Model for comments.
Copyright 2010 D. Robert Adams
"""

from google.appengine.ext import db
from documentModel import DocumentModel

class CommentModel(db.Model):
    author = db.UserProperty(auto_current_user_add=True)# who created this comment
    content = db.TextProperty()                         # comment text
    date = db.DateTimeProperty(auto_now_add=True)       # when created
    document = db.ReferenceProperty(DocumentModel)      # the document to which this comment refers
