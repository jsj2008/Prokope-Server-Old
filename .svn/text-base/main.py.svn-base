#!/usr/bin/env python
""" 
Controller for the main application.
Copyright 2010 D. Robert Adams
"""

import controllers.comment
import controllers.document
import controllers.media
import google.appengine.ext
import google.appengine.ext.webapp
import google.appengine.ext.webapp.util
import models.comment
import models.document
import models.media
import rest
import utility.template_loader 

class MainHandler(google.appengine.ext.webapp.RequestHandler):
	def get(self):
#		global User, Nickname, Url_link
		
#		query = models.document.Document.all()
		
#		if User:
			# Fetch the last 10 documents uploaded by the user.
#			query.filter('author =', User).order('-date')
#		else:
			# Fetch the last 10 documents with no author (special).
#			query.filter('author =', google.appengine.api.users.User("test@example.com")).order('-date')
			
#		docs = query.fetch(10)
		
		# Store the key in the Documents so we can make links to the
		# documents from within the template.  The template doesn't
		# allow us to run functions, e.g., {{doc.key()}}.
#		for doc in docs:
#		    doc.key = str(doc.key())
		
		# Generate the view.
		self.response.out.write( utility.template_loader.TemplateLoader.render_template('index.html') )

application = google.appengine.ext.webapp.WSGIApplication([
    ('/', MainHandler),
    ('/comment', controllers.comment.CommentHandler),
    (r'/document/?(.*)', controllers.document.DocumentHandler),
    ('/rest/.*', rest.Dispatcher),
    (r'/media/?(.*)', controllers.media.MediaHandler),
], debug=True)

# configure the rest dispatcher to know what prefix to expect on request urls
rest.Dispatcher.base_url = "/rest"

# add all models from the current module, and/or...
#rest.Dispatcher.add_models_from_module(__name__)
# add all models from some other module, and/or...
#rest.Dispatcher.add_models_from_module(my_model_module)
# add specific models
#rest.Dispatcher.add_models({
#  "document": Document,
#  "comment": Comment})
# add specific models (with given names) and restrict the supported methods
rest.Dispatcher.add_models({
  "document" : (models.document.Document, rest.READ_ONLY_MODEL_METHODS),
  "comment" : (models.comment.Comment, rest.READ_ONLY_MODEL_METHODS),
  "media" : (models.media.Media, rest.READ_ONLY_MODEL_METHODS) 
})

# use custom authentication/authorization
#rest.Dispatcher.authenticator = MyAuthenticator()
#rest.Dispatcher.authorizer = MyAuthorizer()

def main():
    google.appengine.ext.webapp.util.run_wsgi_app(application)

if __name__ == '__main__':
    main()