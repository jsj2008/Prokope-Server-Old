"""
Controller for handling sidebar uploads.
Copyright 2011 D. Robert Adams
"""

from google.appengine.ext.webapp import RequestHandler
from google.appengine.api import users
from utility.templateLoader import TemplateLoader
from google.appengine.ext import db
from models.sidebarModel import SidebarModel
from xml.dom import minidom
import cgi
import logging

class SidebarHandler(RequestHandler):
   
    """======================================================================
    post - stores sidebar data.
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
            
            # Create a new sidebar model object.
            sidebar = SidebarModel()
            sidebar.content = unicode( self.request.get("sidebar"), "utf-8")
            sidebar.document = db.Key( cgi.escape( self.request.get('doc_key') ) )
            
            # Try to parse the sidebar's XML (at least make sure it's XML).
            dom = minidom.parseString( sidebar.content.encode("UTF-8") )
            
            # Make sure there is a "sidebar" element.  We probably need to make more checks
            # here for more robust upload.
            #if not dom.getElementsByTagName("sidebar"):
            #    raise TypeError("No \"sidebar\" element exists in the sidebar.")
            
            # Store the sidebar.
            sidebar.put()
            
            # Redirect back to the document page.
            self.redirect("/document/" + self.request.get('doc_key') )
        
        except Exception:
            self.response.out.write(
                TemplateLoader.renderError(
                    "An error occurred while uploading your document.  \
                    Please remember that only valid XML documents are allowed to \
                    be uploaded. The specific error message is shown below."
                ))