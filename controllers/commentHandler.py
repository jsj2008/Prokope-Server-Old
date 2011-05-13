"""
Controller for handling comment uploads.
Copyright 2010 D. Robert Adams
"""

from google.appengine.ext.webapp import RequestHandler
from google.appengine.api import users
from utility.templateLoader import TemplateLoader
from google.appengine.ext import db
from models.commentModel import CommentModel
from xml.dom import minidom
import cgi
import logging

class CommentHandler(RequestHandler):
   
    """======================================================================
    post - stores comment data.
    """
    def post(self):
        
        # Only allow posts if the user is logged in.
        user = users.get_current_user()
        if not user:
            self.redirect("/")
        
        try:
            # Make sure we have a document key, otherwise complain.
            if not self.request.get('doc_key'):
                self.response.out.write( TemplateLoader.renderError(
                        "You must supply a valid document id."
                    ))
                return
            
            # Create a new comment.
            comment = CommentModel()
            comment.content = unicode( self.request.get("commentary"), "utf-8")
            comment.document = db.Key( cgi.escape( self.request.get('doc_key') ) )
            
            # Try to parse the comment's XML (at least make sure it's XML).
            dom = minidom.parseString( comment.content.encode("UTF-8") )
            
            # Make sure there is a "commentary" element.  We probably need to make more checks
            # here for more robust upload.
            if not dom.getElementsByTagName("commentary"):
                raise TypeError("No \"commentary\" element exists in the comment.")
            
            # Store the comment.
            comment.put()
            
            # Redirect back to the document page.
            self.redirect("/document/" + self.request.get('doc_key') )
        
        except Exception:
            self.response.out.write(
                TemplateLoader.renderError(
                    "An error occurred while uploading your document.  \
                    Please remember that only valid XML documents are allowed to \
                    be uploaded, and the XML document must have a \"commentary\" element \
                    that contains the main commentary.  The specific error message \
                    is shown below."
                ))