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


class ViewAllMain(webapp2.RequestHandler):
    def get(self):
        try:
            user = users.get_current_user().user_id()
        except:
            return self.redirect("/")

        allcover_query = database.stream.query(database.stream.create_time!=None).order(database.stream.create_time)
        allcover = allcover_query.fetch()
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
            'allcover': allcover,
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
            'streamnames':strname,
        }
        template = JINJA_ENVIRONMENT.get_template('Viewall.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/view', ViewAllMain),
    ('/view_photo',singlestream.ViewPhotoHandler)
        ], debug=True)
