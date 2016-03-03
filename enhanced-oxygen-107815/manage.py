__author__ = 'sm'

import os
import urllib
import Viewall
import Search
import database
import create
import singlestream
import Trending
import Error
import json
import android

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

class MainPage(webapp2.RequestHandler):
    def get(self):
        img_url = self.request.get('img_url')
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            if img_url:
                url = users.create_login_url("/webupload?img_url="+img_url)
            else:
                url = users.create_login_url('/manage')
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,

        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


#
class Manage(webapp2.RequestHandler):
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
        user = users.get_current_user().user_id()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        own_stream = database.stream.query(ndb.AND(database.stream.user_id==user,database.stream.create_time!=None)).order(-database.stream.create_time).fetch()

        sub=database.Subscribe.query(database.Subscribe.user_id==user).fetch()
        list=[]
        for i in sub:
            list.append(i.stream_id)

        substream = database.stream.query().fetch()
        sub_stream=[]
        for j in substream:
            if j.stream_id in list:
                sub_stream.append(j)

        template_values = {
            'own_stream':own_stream,
            'user': user,
            'sub_stream':sub_stream,
            'url': url,
            'url_linktext': url_linktext,
            'streamnames':strname,
        }

        template = JINJA_ENVIRONMENT.get_template('manage.html')
        self.response.write(template.render(template_values))
        print "in manage page, "

class delete(webapp2.RequestHandler):

    def post(self):
        user = users.get_current_user().user_id()

        list=self.request.get_all('delete')

        delete_query = database.stream.query(database.stream.user_id==user).fetch()

        for i in delete_query:
            if(i.stream_id in list):
                i.key.delete()

        deleteimagequery = database.imagedata.query().fetch()
        for j in deleteimagequery:
            if(j.stream_id in list):
                j.key.delete()


        self.redirect('/manage')

class unsubscribe(webapp2.RequestHandler):
    def post(self):
        user=users.get_current_user().user_id()
        list =self.request.get_all('unsubscribe')

        unsub_query = database.Subscribe.query().fetch()

        for i in unsub_query:
            if (i.stream_id in list):
                i.key.delete()

        self.redirect('/manage')

app = webapp2.WSGIApplication([
    ('/',MainPage),
    # ('/login',loginpage)
    ('/createstream', create.Create),
    ('/search', Search.SearchMain),
    ('/createstreamsign', create.CreateStream),
    ('/view',Viewall.ViewAllMain),
    ('/singlestream', singlestream.SingleStreamMain),
    ('/view_photo',singlestream.ViewPhotoHandler),
    ('/upload_photo', singlestream.SingleStream),
    ('/manage', Manage),
    ('/delete', delete),
    ('/unsub', unsubscribe),
    ('/subscribe', singlestream.subscribe),
    ('/Trending',Trending.TrendingHandler),
    ('/email5', Trending.email5),
    ('/email60', Trending.email60),
    ('/email1440', Trending.email1440),
    ('/radio',Trending.RadioHandler),
    ('/error', Error.Error),
    ('/error2', Error.Error2),
    ('/error3', Error.Error3),
    ('/error4', Error.Error4),
    ('/webupload',singlestream.WebUpload),
    ('/webup',singlestream.webuploadhandler),
    ('/viewAllPhotos', android.ViewAllPhotos),
    ('/viewSingle', android.ViewSingle),
    ('/getUploadURL',android.GetUploadURL),
    ('/uploadHandler', android.UploadHandler),

], debug=True)
