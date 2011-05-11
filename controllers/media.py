""" 
Controller for handling multimedia objects.
Copyright 2010 D. Robert Adams
"""

import cgi
import google.appengine.ext
import models.media
import utility.template_loader

class MediaHandler(google.appengine.ext.webapp.RequestHandler):
 
    """======================================================================
    Serves the given media (media_id).
    """   
    def get(self, key):
      media = google.appengine.ext.db.get( key )
      if media.content:
          self.response.headers['Content-Type'] = media.type
          self.response.out.write(media.content)
      else:
          self.error(404)
          
    """======================================================================
    Stores a new media "comment".  Redirects to the document if successful, otherwise
    it displays an error message.
    """
    def post(self, dummy):
        media = models.media.Media()
        media.type = self.request.POST['media_content'].type

        # Make sure only images and audio are uploaded.
        if (not media.type.startswith("image")) and (not media.type.startswith("audio")):
          self.response.out.write( utility.template_loader.TemplateLoader.render_error( "Only image and audio types are supported.") )
          return
  
        media.author = google.appengine.api.users.get_current_user()
        media.document = google.appengine.ext.db.Key( cgi.escape( self.request.get('media_document') ) )      
        media.anchor = cgi.escape( self.request.get('media_anchor') )
        media.title = cgi.escape( self.request.get('media_title') )
        media.content = google.appengine.ext.db.Blob( self.request.get('media_content') )
        media.put()
        
        self.redirect("/document/" + self.request.get('media_document') )
