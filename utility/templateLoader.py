""" 
Utility class to load and render a template.  Automatically fetches the
current user and his nickname.
Copyright 2011 D. Robert Adams
"""

import google.appengine.api.users
import google.appengine.ext.webapp.template
import os
import sys

class TemplateLoader(object):
    
    VIEWS_DIR = "views"
    
    #**********************************************************************
    """ Loads the given template passing it the named values on the argument
       list.  Returns the text of the template.  The "nickname" of the
       user and the login "url_link" is automatically passed to every template.
       
       Typical usage:
           self.response.out.write(
    		    TemplateLoader.render_template(TEMPLATE_FILENAME,
    		        NAME=VARIABLE,
    		        NAME=VARIABLE,
    		        ...
    			))
    """
    @classmethod
    def renderTemplate(cls, template_name, **template_values):
        # Assumes views are in "../views" from here.
        path = os.path.join(os.path.dirname(__file__), '..', TemplateLoader.VIEWS_DIR, template_name)
        user = google.appengine.api.users.get_current_user()
        if user:
            url_link = google.appengine.api.users.create_logout_url("/")
            nickname = user.nickname()
        else:
            url_link = google.appengine.api.users.create_login_url("/")
            nickname = None
         
        template_values['nickname'] = nickname
        template_values['url_link'] = url_link
        return google.appengine.ext.webapp.template.render(path, template_values)
        
    #**********************************************************************
    """Renders the error template.  The only parameter required is the
       error message you want to display."""
    @classmethod
    def renderError(cls, message):
        user = google.appengine.api.users.get_current_user()
        if user:
            url_link = google.appengine.api.users.create_logout_url("/")
            nickname = user.nickname()
        else:
            url_link = google.appengine.api.users.create_login_url("/")
            nickname = None
            
        # Grab the last exception that happened.
        exc_class, exc_value, trbk = sys.exc_info()
        
        # Assumes views are in "../views" from here.
        path = os.path.join(os.path.dirname(__file__), '..', TemplateLoader.VIEWS_DIR, "error.html")
        
        # Pack up data for the template to use.
        template_values = {}
        if exc_class:
            template_values['exception_details'] = exc_class.__name__ + ": " + str(exc_value)
        else:
            template_values['exception_details'] = ""
        template_values['error_message'] = message
        template_values['nickname'] = nickname
        
        # Render the template and return it.
        return google.appengine.ext.webapp.template.render(path, template_values)       