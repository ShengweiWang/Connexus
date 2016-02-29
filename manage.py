import os
import webapp2
import jinja2
import database
import json
from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

'''
Pages
'''

class LoginPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Welcome!" + user.nickname()
        else:
            url = users.create_login_url('/')
            url_linktext = 'Login'

        template_values = {

            'url': url,
            'url_linktext': url_linktext,

        }

        template = JINJA_ENVIRONMENT.get_template('Login.html')
        self.response.write(template.render(template_values))

class ManagementPage(webapp2.RequestHandler):
    def get(self):
        try:
            user = users.get_current_user().user_id()
        except:
            return self.redirect("/")

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Welcome!" + users.get_current_user().nickname()
        else:
            url = users.create_login_url('/')
            url_linktext = 'Login'

        own_stream = database.Stream.query(
                ndb.AND(database.Stream.user_id==user,database.Stream.create_time!=None))\
            .order(-database.Stream.create_time).fetch()

        sub_stream = database.Subscribe.query(database.Subscribe.user_id==user).fetch()

        template_values = {
            'own_stream': own_stream,
            'user': user,
            'sub_stream': sub_stream,
            'url':url,
            'url_linktext':url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('Management.html')
        self.response.write(template.render(template_values))


'''
Action
'''
class DeleteStream(webapp2.RequestHandler):
    def post(self):
        try:
            user = users.get_current_user.user_id()
        except:
            return self.redirect("/")
        deleteList = self.request.get_all('delete')

        deleteStreamQuery = database.Stream.query(database.Stream.user_id==user).fetch()
        for i in deleteStreamQuery:
            if(i.stream_id in deleteList):
                i.key.delete()

        deleteImageQuery = database.Imagedata.query().fetch()
        for j in deleteImageQuery:
            if(j.stream_id in deleteList):
                j.key.delete()
        self.redirect("/manage")

class UnsubscribeStream(webapp2.RequestHandler):
    def post(self):
        try:
            user = users.get_current_user.user_id()
        except:
            return self.redirect("/")
        unsubList = self.request.get_all('unsubscribe')

        unsubStreamQuery = database.Stream.query(database.Stream.user_id==user).fetch()
        for i in unsubStreamQuery:
            if(i.stream_id in unsubList):
                i.key.delete()
        self.redirect("/manage")

app = webapp2.WSGIApplication([
    ('/',LoginPage),
    ('/manage',ManagementPage),
    ('/deleteStream',DeleteStream),
    ('/unsubscribeStream',UnsubscribeStream),
],debug=True)