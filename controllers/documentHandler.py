""" 
Controller for handling documents.
Copyright 2011 D. Robert Adams
"""

from google.appengine.ext.webapp import RequestHandler
from google.appengine.ext import db
from google.appengine.api import users
from models.documentModel import DocumentModel
from google.appengine import api
from utility.templateLoader import TemplateLoader
from xml.dom import minidom


class DocumentHandler(RequestHandler):

    """======================================================================
       HTTP GET Handler.  Displays a document.
       We may receive the key of the document to show."""
    def get(self, keyStr):
        
        self.response.headers['Content-Type'] = "application/xml"
        
        # If we have a document key, fetch and display the document.
        if keyStr:
            doc = db.get(keyStr) 
            if not doc:
                self.response.out.write("Error")
            else:
                self.response.out.write(doc.content)
            return
            
        # If no document key is given, display a list of all owned documents.
        user = users.get_current_user()
        q = DocumentModel.all().filter("author =", user).order("title")
        results = q.fetch(100)
        self.response.out.write("<list>")
        for p in results:
            self.response.out.write("""
                <document>
                    <title>%s</title>
                    <key>%s</key>
                </document>""" % (p.title, p.key()) )
        self.response.out.write("</list>")
                
       
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
