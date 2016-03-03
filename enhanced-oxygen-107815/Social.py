__author__ = 'sm'

import os
import create
import urllib
import database
import singlestream
import json

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Social(webapp2.RequestHandler):
    def get(self):
        try:
            user = users.get_current_user().user_id()
        except:
            return self.redirect("/")


        sname=[]
        astream=database.stream.query().fetch()
        for s in astream:
            sname.append(s.stream_id)
        strname=json.dumps(sname)

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'streamnames':strname,
        }
        template = JINJA_ENVIRONMENT.get_template('social.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/social', Social),
        ], debug=True)
