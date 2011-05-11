#!/usr/bin/env python
""" 
Controller for the main application.
Copyright 2011 D. Robert Adams
"""

from controllers.documentHandler import DocumentHandler
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models.commentModel import CommentModel
from models.documentModel import DocumentModel
from models.mediaModel import MediaModel
import rest
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
    ('/rest/.*', rest.Dispatcher),
#    ('/comment', controllers.comment.CommentHandler),
#    (r'/media/?(.*)', controllers.media.MediaHandler),
], debug=True)

# Configure the rest dispatcher to know what prefix to expect on request urls
rest.Dispatcher.base_url = "/rest"

# Add models to the restful interface.
#  "document": Document,
#  "comment": Comment})
rest.Dispatcher.add_models({
  "document" : (DocumentModel, rest.READ_ONLY_MODEL_METHODS),
#  "comment" : (CommentModel, rest.READ_ONLY_MODEL_METHODS),
#  "media" : (MediaModel, rest.READ_ONLY_MODEL_METHODS) 
})


def main():
    webapp.util.run_wsgi_app(application)


if __name__ == '__main__':
    main()