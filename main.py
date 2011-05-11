#!/usr/bin/env python
""" 
Controller for the main application.
Copyright 2011 D. Robert Adams
"""

import logging
from controllers.documentHandler import DocumentHandler
from controllers.restHandler import RestHandler
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models.commentModel import CommentModel
from models.documentModel import DocumentModel
from models.mediaModel import MediaModel
from utility.templateLoader import TemplateLoader


class MainHandler(webapp.RequestHandler):
    """Handles the 'main' (empyt) URL."""
    
    def get(self):
		"""Generates the home page for the application."""
		self.response.out.write( TemplateLoader.renderTemplate('index.html') )


# Set up the application handlers.
application = webapp.WSGIApplication([
    ('/', MainHandler),
    (r'/document/?(.*)', DocumentHandler),
    (r'/rest/?(\w*)/?(\w*)', RestHandler),
#    ('/comment', controllers.comment.CommentHandler),
#    (r'/media/?(.*)', controllers.media.MediaHandler),
], debug=True)



def main():
    logging.getLogger().setLevel(logging.DEBUG)
    webapp.util.run_wsgi_app(application)


if __name__ == '__main__':
    main()