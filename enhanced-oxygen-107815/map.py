import os
import database
import urllib
import json
from datetime import datetime

from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Map(webapp2.RequestHandler):
    def post(self):

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

        stream_name = self.request.get('stream_name')
        user = users.get_current_user().user_id()

        streaming = database.stream.query().fetch()

        # exist = database.stream.query(database.stream.stream_id==stream_name).fetch()
        #
        # if not exist:
        #     return self.redirect("/error2")

        # own=0
        # for mystream in streaming:
        #     if mystream.stream_id==stream_name and mystream.user_id!=user:
        #         mystream.numview = mystream.numview+1
        #         mystream.view.append(datetime.now())
        #         own=1
        #         mystream.put()
        #         break

        allimage_query = database.imagedata.query(ndb.AND(
            database.imagedata.stream_id == stream_name,database.imagedata.date!=None)).order(database.imagedata.date)
        allimage = allimage_query.fetch()

        numbers=len(allimage)


        urllist=[]
        daysago=[]
        location=[]
        for i in allimage:
            urllist.append(i.url)
            day = int((datetime.now()-i.date).days)
            daysago.append(day)
            location.append(i.position)
        url=json.dumps(urllist)
        position=json.dumps(location)

        upload_url = blobstore.create_upload_url('/upload_photo')

        template_values = {
            # 'more':more,
            'daysago':daysago,
            'urllist':url,
            'numbers':numbers,
            'allimage': allimage,
            'stream_name': urllib.quote_plus(stream_name),
            'upload_url':upload_url,
            'url': url,
            'url_linktext': url_linktext,
            'streamnames':strname,
            'position':position
        }

        # if own==1:
        #     template = JINJA_ENVIRONMENT.get_template('Single_stream.html')
        #     self.response.write(template.render(template_values))
        # elif own==0:
        template = JINJA_ENVIRONMENT.get_template('map.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/map', Map),
        ], debug=True)