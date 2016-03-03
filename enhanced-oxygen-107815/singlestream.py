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

class SingleStreamMain(webapp2.RequestHandler):
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

        stream_name = self.request.get('stream_name')
        more=self.request.get('more')
        user = users.get_current_user().user_id()

        streaming = database.stream.query().fetch()

        exist = database.stream.query(database.stream.stream_id==stream_name).fetch()

        if not exist:
            return self.redirect("/error2")

        own=0
        for mystream in streaming:
            if mystream.stream_id==stream_name and mystream.user_id!=user:
                mystream.numview = mystream.numview+1
                mystream.view.append(datetime.now())
                own=1
                mystream.put()
                break

        allimage_query = database.imagedata.query(ndb.AND(
            database.imagedata.stream_id == stream_name,database.imagedata.date!=None)).order(database.imagedata.date)

        if more=='1':
            allimage = allimage_query.fetch()
        else:
            allimage = allimage_query.fetch(3)

        upload_url = blobstore.create_upload_url('/upload_photo')

        template_values = {
            'more':more,
            'allimage': allimage,
            'stream_name': urllib.quote_plus(stream_name),
            'upload_url':upload_url,
            'url': url,
            'url_linktext': url_linktext,
            'streamnames':strname,
        }

        if own==1:
            template = JINJA_ENVIRONMENT.get_template('Single_stream.html')
            self.response.write(template.render(template_values))
        elif own==0:
            template = JINJA_ENVIRONMENT.get_template('Single_stream_owner.html')
            self.response.write(template.render(template_values))

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
        more=self.request.get('more')
        user = users.get_current_user().user_id()

        streaming = database.stream.query().fetch()

        exist = database.stream.query(database.stream.stream_id==stream_name).fetch()

        if not exist:
            return self.redirect("/error2")

        own=0
        for mystream in streaming:
            if mystream.stream_id==stream_name and mystream.user_id!=user:
                mystream.numview = mystream.numview+1
                mystream.view.append(datetime.now())
                own=1
                mystream.put()
                break

        allimage_query = database.imagedata.query(ndb.AND(
            database.imagedata.stream_id == stream_name,database.imagedata.date!=None)).order(database.imagedata.date)

        if more=='1':
            allimage = allimage_query.fetch()
        else:
            allimage = allimage_query.fetch(3)

        upload_url = blobstore.create_upload_url('/upload_photo')

        template_values = {
            'more':more,
            'allimage': allimage,
            'stream_name': urllib.quote_plus(stream_name),
            'upload_url':upload_url,
            'url': url,
            'url_linktext': url_linktext,
            'streamnames':strname,
        }

        if own==1:
            template = JINJA_ENVIRONMENT.get_template('Single_stream.html')
            self.response.write(template.render(template_values))
        elif own==0:
            template = JINJA_ENVIRONMENT.get_template('Single_stream_owner.html')
            self.response.write(template.render(template_values))

class SingleStream(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
            stream_name = self.request.get('stream')

            user = users.get_current_user().user_id()
            streaming = database.stream.query(
            ancestor = ndb.Key('User', user)).fetch()



            number= len(self.get_uploads())
            for i in range(number):

                upload = self.get_uploads()[i]
                user_photo = database.imagedata(parent=ndb.Key('User', user)) #everyone can upload
                user_photo.blob_key =upload.key()
                user_photo.comment = self.request.get('comment')
                user_photo.name = self.request.get('name')
                user_photo.stream_id = stream_name
                user_photo.url = images.get_serving_url(upload.key())
                user_photo.user_id = user

                for mystream in streaming:
                    if mystream.stream_id==stream_name:
                        if(mystream.cover_key==None):
                            mystream.cover_key=upload.key()
                            mystream.cover_url =images.get_serving_url(upload.key())


                        mystream.blob_key.append(upload.key())
                        user_photo.put()
                        mystream.numberofpic = mystream.numberofpic + 1
                        last_add = str(datetime.now())
                        mystream.last_add=last_add[:19]
                        mystream.put()
                        break



            direct = {'stream_name': self.request.get('stream')}
            direct = urllib.urlencode(direct)
            self.redirect('/singlestream?' + direct)


class subscribe(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user().user_id()
        user_email= users.get_current_user().email()
        stream_name = self.request.get('stream_name')

        sub = database.Subscribe()
        sub.stream_id=stream_name
        sub.user_id=user
        sub.user_email=user_email
        sub.put()

        direct = {'stream_name': self.request.get('stream_name')}
        direct = urllib.urlencode(direct)

        self.redirect('/singlestream?' + direct)


class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        blob = self.request.get('blob')
        self.send_blob(blob)

class WebUpload(webapp2.RequestHandler):
    def get(self):
        img_url = self.request.get('img_url')
        try:
            user = users.get_current_user().user_id()
        except:
            return self.redirect("/?img_url="+img_url)

        user = users.get_current_user().user_id()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            self.redirect(users.create_login_url(self.request.uri))



        sname=list()
        astream=database.stream.query(database.stream.user_id == user).fetch()
        for s in astream:
            sname.append(s.stream_id)
        strname=json.dumps(sname)
        # form = cgi.FieldStorage()
        # streamname =  form.getvalue('streamnamefield')
        # direct1 = {'stream_name': streamname}
        # direct1 = urllib.urlencode(direct1)
        # direct2 = {'img_url': img_url}
        # direct2 = urllib.urlencode(direct2)
        # upload_url = '/webup?' + direct1+'&'+direct2
        upload_url = blobstore.create_upload_url('/webup')
        template_values = {
            'img_url': img_url,
            'url': url,
            'url_linktext': url_linktext,
            'streamnames':strname,
            'upload_url': upload_url
        }
        template = JINJA_ENVIRONMENT.get_template('webupload.html')
        self.response.write(template.render(template_values))

class webuploadhandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):

            stream_name = self.request.get('streamnamefield')

            user = users.get_current_user().user_id()
            streaming = database.stream.query(
            database.stream.user_id==user).fetch()

            user_photo = database.imagedata(parent=ndb.Key('User', user)) #everyone can upload
            user_photo.comment = self.request.get('comments')
            user_photo.stream_id = stream_name
            user_photo.url = self.request.get('url')
            user_photo.user_id = user
            place = self.request.get('position')
            place2=place.replace(',','%')
            user_photo.position=place2


            owns=1
            for mystream in streaming:
                if mystream.stream_id==stream_name:
                    # if(mystream.numberofpic==0):
                    #     mystream.cover_url =images.get_serving_url(upload.key())


                    # mystream.blob_key.append(upload.key())
                    user_photo.put()
                    mystream.numberofpic = mystream.numberofpic + 1
                    last_add = str(datetime.now())
                    mystream.last_add=last_add[:19]
                    mystream.put()
                    owns=0
                    break

            if owns==1:
                return self.redirect('/error4')


            direct = {'stream_name': self.request.get('streamnamefield')}
            direct = urllib.urlencode(direct)
            self.redirect('/singlestream?' + direct)

app = webapp2.WSGIApplication([
    ('/singlestream', SingleStreamMain),
    ('/view_photo',ViewPhotoHandler),
    ('/upload_photo', SingleStream),
    ('/subscribe',subscribe),
    ('/webupload',WebUpload),
    ('/webup',webuploadhandler)

        ], debug=True)