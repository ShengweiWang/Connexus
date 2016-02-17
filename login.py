import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb


import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')


        self.response.out.write("""
              <form action="/manage">
                <div>
                  ID:
                  <input type="text" name="userid"></input>

                  email:
                  <input type="text" name="useremail"></input>

                </div>
                <div><input type="submit" value="Login"></div>
              </form>
              <hr>

            </body>
          </html>""")

app = webapp2.WSGIApplication([('/', MainPage),('/index.html',MainPage)],
                              debug=True)
