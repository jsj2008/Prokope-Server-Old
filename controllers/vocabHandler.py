"""
Controller for handling vocabulary uploads.
Copyright 2011 D. Robert Adams
"""

from google.appengine.ext.webapp import RequestHandler
from google.appengine.api import users
from utility.templateLoader import TemplateLoader
from google.appengine.ext import db
from models.vocabModel import VocabModel
from xml.dom import minidom
import cgi
import logging

class VocabHandler(RequestHandler):
   
    """======================================================================
    post - stores vocab data.
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
            
            # Create a new vocab model object.
            vocab = VocabModel()
            vocab.content = unicode( self.request.get("vocabulary"), "utf-8")
            vocab.document = db.Key( cgi.escape( self.request.get('doc_key') ) )
            
            # Try to parse the vocab's XML (at least make sure it's XML).
            dom = minidom.parseString( vocab.content.encode("UTF-8") )
            
            # Make sure there is a "vocabulary" element.  We probably need to make more checks
            # here for more robust upload.
            if not dom.getElementsByTagName("vocabulary"):
                raise TypeError("No \"vocabulary\" element exists in the vocab.")
            
            # Store the vocab.
            vocab.put()
            
            # Redirect back to the document page.
            self.redirect("/document/" + self.request.get('doc_key') )
        
        except Exception:
            self.response.out.write(
                TemplateLoader.renderError(
                    "An error occurred while uploading your document.  \
                    Please remember that only valid XML documents are allowed to \
                    be uploaded, and the XML document must have a \"vocabulary\" element \
                    that contains the main vocabulary.  The specific error message \
                    is shown below."
                ))