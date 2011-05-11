""" 
Controller for handling RESTful (from the iPad app) requests.
Copyright 2011 D. Robert Adams
"""
import logging

from google.appengine.ext.webapp import RequestHandler
from google.appengine.ext import db
from google.appengine.api import users
from models.documentModel import DocumentModel
from google.appengine import api
from utility.templateLoader import TemplateLoader
from xml.dom import minidom


class RestHandler(RequestHandler):

   #**************************************************************************
    def get(self, model, key):
        """Main handler for GET requests. args[0] is the name of the model
        to use (e.g., document). args[1] may be the key of the item to fetch."""
            
        if model == "document":
            self.getDocument(key)
            
    #**************************************************************************
    def getDocument(self, key):
        """RESTful handler for the DocumentModel."""
        
        self.response.headers['Content-Type'] = "application/xml"
        
        # If we have a document key, fetch and display the document.
        if key:
            doc = db.get(key) 
            if not doc:
                self.response.out.write("Error")
            else:
                self.response.out.write("""
                <document>
                    <title>%s</title>
                    <author>%s</author>
                    <content>%s</content>
                </document>
                """ % (doc.title, doc.author, doc.content))
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

