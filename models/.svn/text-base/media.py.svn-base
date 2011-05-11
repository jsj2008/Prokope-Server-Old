""" 
Model for media "comments".
Copyright 2010 D. Robert Adams
"""

from google.appengine.ext import db
from google.appengine.ext import blobstore


import document

class Media(db.Model):
    author = db.UserProperty()                          # who created this comment
    type = db.StringProperty()                          # MIME type
    title = db.StringProperty()                         # title of the media
    content = db.BlobProperty()                         # media content
    date = db.DateTimeProperty(auto_now_add=True)       # when created
    document = db.ReferenceProperty(document.Document)  # the document to which this comment refers
    anchor = db.StringProperty()                        # the element in the document to which this comment refers 
