__author__ = 'sm'

import os
import create
import urllib
import database
import singlestream

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Error(webapp2.RequestHandler):
    def get(self):
        template_values = {
        }
        template = JINJA_ENVIRONMENT.get_template('Error.html')
        self.response.write(template.render(template_values))

class Error2(webapp2.RequestHandler):
    def get(self):
        template_values = {
        }
        template = JINJA_ENVIRONMENT.get_template('Error2.html')
        self.response.write(template.render(template_values))

class Error3(webapp2.RequestHandler):
    def get(self):
        template_values = {
        }
        template = JINJA_ENVIRONMENT.get_template('Error3.html')
        self.response.write(template.render(template_values))

class Error4(webapp2.RequestHandler):
    def get(self):
        template_values = {
        }
        template = JINJA_ENVIRONMENT.get_template('Error4.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/error', Error),
    ('/error2', Error2),
    ('/error3', Error3),
    ('/error4', Error4),
        ], debug=True)
