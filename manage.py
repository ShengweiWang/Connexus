import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import datamodel
import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):

        userid=self.request.getParameter("userid")
        curUser=User.query(id=userid)
        if curUser:
            self.response.out.write(curUser)
        else:
            curUser=User(id=userid)
            curUser.put()
        self.response.out.write(curUser)





app = webapp2.WSGIApplication([
    ('/manage',MainPage)
], debug=True)
