""" 
Controller for handling documents.
Copyright 2011 D. Robert Adams
"""

from google.appengine.ext.webapp import RequestHandler
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine import api
from models.documentModel import DocumentModel
from models.commentModel import CommentModel
from models.vocabModel import VocabModel
from models.sidebarModel import SidebarModel
import re
from utility.templateLoader import TemplateLoader
from xml.dom import minidom

import logging


class DocumentHandler(RequestHandler):
    
    #*******************************************************************************************
    def getDocumentComponents(self, key):
        """Gets the document, commentary, vocabulary, and sidebar data corresponding to the given
           document key. Returns a hash {"document", "commentary", "vocabulary", and "sidebar"} of
           model objects.
        """
        
        retval = {}
        
        # Fetch the document
        doc = db.get(key) 
        # Force a line break after each line.
        doc.content = doc.content.replace("</l>", "</l><br/>")
        # Make sure that "indent"ed lines are indented.
        #doc.content = doc.content.replace('rend="indent">', 'rend="indent">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
	# &#160; is the XML version of &nbsp.
        doc.content = doc.content.replace('rend="indent">', 'rend="indent">&#160;&#160;&#160;&#160;&#160;&#160;')
	# Convert words (w) to hyperlinks (a href).
	# (?ims) turns on the case-insensitive, multiline, dot matches newline flags.
	doc.content = re.sub(r'(?ims)<w\s+id="([0-9.]+)">([^>]+)</w>', r'<a href="\1">\2</a>', doc.content)
        retval["document"] = doc
        
        # Fetch the commentary for this document.
        q = CommentModel.all().filter("document = ", db.Key(key))
        results = q.fetch(1)
        if len(results) > 0:
            comment = results[0].content
        else:
            comment = "None"
        # Convert "comment" to "li" (list items).
        comment = comment.replace("<comment ", "<li ").replace("</comment>", "</li>")
        retval["commentary"] = comment
                
        # Fetch the vocabulary for this document.
        q = VocabModel.all().filter("document = ", db.Key(key))
        results = q.fetch(1)
        if len(results) > 0:
            vocab = results[0].content
        else:
            vocab = "None"
        vocab = vocab.replace("<vocab ", "<li ").replace("</vocab>", "</li>")
        retval["vocabulary"] = vocab

        # Fetch the sidebar data for this document.
        q = SidebarModel.all().filter("document = ", db.Key(key))
        results = q.fetch(1)
        if len(results) > 0:
            sidebar = results[0].content
        else:
            sidebar = "None"
        retval["sidebar"] = sidebar
        
        return retval        
        

    """======================================================================
       HTTP GET Handler.  Displays a document.
       We must receive the key of the document to show."""
    def get(self, key):  
        
        docElements = self.getDocumentComponents(key)  
          
        doc = docElements["document"] 
        comment = docElements["commentary"]
        vocab = docElements["vocabulary"]
        sidebar = docElements["sidebar"]
        
        # Render the document display view.
        self.response.out.write(TemplateLoader.renderTemplate('show.html', 
            document_id=key, document_content=doc.content, document_title=doc.title,
            commentary=comment, vocabulary=vocab, sidebar=sidebar))

                
       
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
            document.content = unicode( self.request.get("doc_content"), "utf-8")
            #self.request.get("doc_content")

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
