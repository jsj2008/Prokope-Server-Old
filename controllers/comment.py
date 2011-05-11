""" 
Controller for handling comment uploads.
Copyright 2010 D. Robert Adams
"""

import cgi
import xml.dom.minidom
import google.appengine.api
import google.appengine.ext
import models.comment
import utility.template_loader

class CommentHandler(google.appengine.ext.webapp.RequestHandler):

    """======================================================================
    Converts the given list of nodes into an XML string.
    """
    def nodeListToXMLString(self, nodelist):
        rc = ""
        for node in nodelist:
            rc = rc + node.toxml()
        return rc

    """======================================================================
    post - stores comment data.
    """      
    def post(self):
        try:            
            # Make sure we have a document key, otherwise complain.
            if not self.request.get('doc_key'):
                self.response.out.write(
                    utility.template_loader.TemplateLoader.render_error(
                        "You must supply a valid document id."
                    ))
                return

            # Parse the comment XML.  It should consist of a "commentary" element
            # with zero or more "comment" elements.
            for e_comment in xml.dom.minidom.parseString( self.request.get("commentary") ).getElementsByTagName('comment'):
    
                # Build a Comment object.
                comment = models.comment.Comment()
    
                # Fill in the author and document id.
                comment.author = google.appengine.api.users.get_current_user()
                comment.document = google.appengine.ext.db.Key( cgi.escape( self.request.get('doc_key') ) )
                comment.public = True
    
                # Gather comment data from the incoming XML.
                if e_comment.attributes:
                    comment.anchor = e_comment.attributes["ref"].value
                    comment.type = e_comment.attributes["type"].value
                    if "title" in e_comment.attributes.keys():
                        comment.title = e_comment.attributes["title"].value
                    comment.content = self.nodeListToXMLString(e_comment.childNodes)
        
                # Store the comment.
                comment.put()
        
                # Go back to the document.
                self.redirect("/document/" + self.request.get('doc_key') )
        except Exception:
            self.response.out.write(
                utility.template_loader.TemplateLoader.render_error(
                    "An error occurred while uploading your document.  \
                    Please remember that only valid XML documents are allowed to \
                    be uploaded, and the XML document must have a \"commentary\" element \
                    that contains the main commentary.  The specific error message \
                    is shown below."
                ))