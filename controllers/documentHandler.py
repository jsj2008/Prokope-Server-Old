""" 
Controller for handling documents.
Copyright 2011 D. Robert Adams
"""

from google.appengine.ext.webapp import RequestHandler
from models.documentModel import DocumentModel
from google.appengine import api
from utility.templateLoader import TemplateLoader
from xml.dom import minidom

class DocumentHandler(RequestHandler):

    """======================================================================
       HTTP GET Handler.  Displays a document.
       Should receive "id" with the key of the document to show."""
    """    def get(self, keyStr):
        self.response.out.write(
            utility.template_loader.TemplateLoader.render_template('show.html') )
            """
       
    """======================================================================
       Handles the uploading of new documents.
    """
    def post(self, dummy):
        
        # Only allow posts if the user is logged in.
        user = api.users.get_current_user()
        if not user:
            self.redirect("/")
            
        try:
            # Create a new document.
            document = DocumentModel()
            document.title = self.request.get("doc_title")
            document.content = self.request.get("doc_content")

            # Try to parse the document's XML (at least make sure it's XML).
            dom_doc = minidom.parseString( document.content.encode("UTF-8") )

            # Make sure there is a "body" element.  We probably need to make more checks
            # here for more robust upload.
            if not dom_doc.getElementsByTagName("body"):
                raise TypeError("No \"body\" element exists in the document.")

            # Store the document.
            document.put()
            
            # Redirect back to the home page.
            self.redirect("/")

        except Exception:
            self.response.out.write(
    		    TemplateLoader.renderError(
                    "An error occurred while uploading your document.  \
                    Please remember that only valid XML documents are allowed to \
                    be uploaded, and the XML document must have a \"body\" element \
                    that contains the main content.  The specific error message \
                    is shown below."
    	    ))
