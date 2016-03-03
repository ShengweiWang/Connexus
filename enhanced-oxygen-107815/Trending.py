__author__ = 'sm'

import os
import database
import urllib
import logging
import json
from datetime import datetime

from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import jinja2
import webapp2
#input not add

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class TrendingHandler(webapp2.RequestHandler):
    def get(self):

        try:
            user = users.get_current_user().user_id()
        except:
            return self.redirect("/")



        streams = database.stream.query().fetch()

        for stream in streams:
            view_list=[]
            for view_ in stream.view:
                if int((datetime.now()- view_).seconds) <int('3600'):
                    view_list.append(1)
            stream.view_in_hour=len(view_list)
            stream.put()

        streaming = database.stream.query().order(-database.stream.view_in_hour).fetch(3)

        sname=[]
        astream=database.stream.query().fetch()
        for s in astream:
            sname.append(s.stream_id)
        strname=json.dumps(sname)

        user = users.get_current_user()
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
                # 'nav_links': USER_NAV_LINKS,
                # 'path': os.path.basename(self.request.path).capitalize(),
                # 'user_id': self.request.get('user_id'),
            'streams': streaming,
            'streamnames':strname,
        }


        template = JINJA_ENVIRONMENT.get_template('Trending.html')
        self.response.write(template.render(template_values))


class email5(webapp2.RequestHandler):
     def get(self):
        streams = database.stream.query().fetch()

        for stream in streams:
            view_list=[]
            for view_ in stream.view:
                if (view_ - datetime.now()).seconds<'3600':
                    view_list.append(1)
            stream.view_in_hour=len(view_list)
            stream.put()

        streaming = database.stream.query().order(-database.stream.view_in_hour).fetch(3)

        freq=database.frequency.query().fetch()
        for fre in freq:
            frequ=fre.frequency
            if frequ== '5':
                mail.send_mail(sender="Miniproject :: info <sunming2725@gmail.com>",
                to=str(fre.user_email),
                subject="Trending streams of connexus in the past hour",
                body="Checkout the three most trending streams!\n"
                     +streaming[0].stream_id + ":"+ str(streaming[0].view_in_hour)+'\n'
                     +streaming[1].stream_id + ":"+ str(streaming[1].view_in_hour)+'\n'
                     +streaming[2].stream_id + ":"+ str(streaming[2].view_in_hour))


        # self.redirect('/Trending')

class email60(webapp2.RequestHandler):
    def get(self):
        streams = database.stream.query().fetch()

        for stream in streams:
            view_list=[]
            for view_ in stream.view:
                if (view_ - datetime.now()).seconds<'3600':
                    view_list.append(1)
            stream.view_in_hour=len(view_list)
            stream.put()

        streaming = database.stream.query().order(-database.stream.view_in_hour).fetch(3)

        freq=database.frequency.query().fetch()
        for fre in freq:
            frequ=fre.frequency
            if frequ== '60':
                mail.send_mail(sender="Miniproject :: info <sunming2725@gmail.com>",
                to=str(fre.user_email),
                subject="Trending streams of connexus in the past hour",
                body="Checkout the three most trending streams!\n"
                     +streaming[0].stream_id + ":"+ str(streaming[0].view_in_hour)+'\n'
                     +streaming[1].stream_id + ":"+ str(streaming[1].view_in_hour)+'\n'
                     +streaming[2].stream_id + ":"+ str(streaming[2].view_in_hour))



class email1440(webapp2.RequestHandler):
    def get(self):
        streams = database.stream.query().fetch()

        for stream in streams:
            view_list=[]
            for view_ in stream.view:
                if (view_ - datetime.now()).seconds<'3600':
                    view_list.append(1)
            stream.view_in_hour=len(view_list)
            stream.put()

        streaming = database.stream.query().order(-database.stream.view_in_hour).fetch(3)

        freq=database.frequency.query().fetch()
        for fre in freq:
            frequ=fre.frequency
            if frequ== '1440':
                mail.send_mail(sender="Miniproject :: info <sunming2725@gmail.com>",
                to=str(fre.user_email),
                subject="Trending streams of connexus in the past hour",
                body="Checkout the three most trending streams!\n"
                     +streaming[0].stream_id + ":"+ str(streaming[0].view_in_hour)+'\n'
                     +streaming[1].stream_id + ":"+ str(streaming[1].view_in_hour)+'\n'
                     +streaming[2].stream_id + ":"+ str(streaming[2].view_in_hour))

        # self.redirect('/Trending')

class RadioHandler(webapp2.RequestHandler):
    def post(self):
        freq=self.request.get('freq')
        user=users.get_current_user()

        fff=database.frequency.query().fetch()
        for f in fff:
            if f.user_id==user.user_id():
                f.frequency=freq
                f.put()
                return self.redirect('/Trending')

        newf=database.frequency()
        newf.user_id=user.user_id()
        newf.user_email=user.email()
        newf.frequency=freq

        newf.put()
        self.redirect('/Trending')

app = webapp2.WSGIApplication([
    ('/Trending', TrendingHandler),
    ('/email5', email5),
    ('/email60', email60),
    ('/email1440', email1440),
    ('/radio',RadioHandler)
        ], debug=True)