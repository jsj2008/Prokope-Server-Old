""" 
Model for comments.
Copyright 2010 D. Robert Adams
"""

from google.appengine.ext import db
import document

class Comment(db.Model):
    author = db.UserProperty()                          # who created this comment
    type = db.StringProperty()                          # what kind of comment
    title = db.StringProperty()                         # title for this comment (optional)
    content = db.TextProperty()                         # comment text
    date = db.DateTimeProperty(auto_now_add=True)       # when created
    document = db.ReferenceProperty(document.Document)  # the document to which this comment refers
    anchor = db.StringProperty()                        # the element in the document to which this comment refers 
    public = db.BooleanProperty()                       # is this comment public?
