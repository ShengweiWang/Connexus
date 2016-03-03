__author__ = 'sm'
import os
import urllib
import singlestream
import Viewall
import create
import database
import json

from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime
from google.appengine.api import search

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# Default_owner_name = 'Anonymous'

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.


class SearchMain(webapp2.RequestHandler):
    def get(self):
        try:
            user = users.get_current_user().user_id()
        except:
            return self.redirect("/")
        searchname = self.request.get('searchfield')

        select=[]
        sname=list()
        astream=database.stream.query().fetch()
        for s in astream:
            sname.append(s.stream_id)
        strname=json.dumps(sname)
        # fout=open('streamname.txt', 'w')
        # json.dump(sname,fout)
        stream_query = database.stream.query(database.stream.stream_id==searchname).fetch()
        for i in stream_query:
            select.append(i)


        number=len(select)


        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'results': select,
            'searchname':searchname,
            'number':number,
            'url': url,
            'url_linktext': url_linktext,
            'streamnames':strname,
        }

        template = JINJA_ENVIRONMENT.get_template('Search.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/search', SearchMain)
        ], debug=True)
