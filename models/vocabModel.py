""" 
Model for vocabulary.
Copyright 2011 D. Robert Adams
"""

from google.appengine.ext import db
from documentModel import DocumentModel

class VocabModel(db.Model):
    author = db.UserProperty(auto_current_user_add=True)# who created this comment
    content = db.TextProperty()                         # vocabulary text
    date = db.DateTimeProperty(auto_now_add=True)       # when created
    document = db.ReferenceProperty(DocumentModel)      # the document to which this vocabulary refers
