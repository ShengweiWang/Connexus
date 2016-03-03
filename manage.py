import os
import webapp2
import jinja2
import database
import urllib
import json
from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
import Image
import cgi
import urllib


from google.appengine.api import images

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


        own_stream = database.Stream.query().fetch()
        print(own_stream)

        #own_stream = database.Stream.query(ndb.AND(database.Stream.user_id==user,database.Stream.create_time!=None)).order(-database.Stream.create_time).fetch()
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

class CreateStreamPage(webapp2.RequestHandler):
    def get(self):
        # guestbook_name = self.request.get('guestbook_name',
        #                                   DEFAULT_GUESTBOOK_NAME)
        try:
            user = users.get_current_user().user_id()
        except:
            return self.redirect("/")
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user':user,
            'url': url,
            'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('Create Stream.html')
        self.response.write(template.render(template_values))
class ViewAllPage(webapp2.RequestHandler):
    def get(self):
        try:
            user = users.get_current_user().user_id()
        except:
            return self.redirect("/")
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        streamList = database.Stream.query().fetch()

        template_values = {
            'allStream':streamList,
            'url': url,
            'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('View All Streams.html')
        self.response.write(template.render(template_values))

class SingleStreamPage(webapp2.RequestHandler):
    def get(self):
        try:
            user = users.get_current_user().user_id()
        except:
            return self.redirect("/")
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        streamkey = self.request.get('curstream')
        streaming = database.Stream.query().fetch()

        for stream in streaming:
            if(stream.key.id()==streamkey):
                break
        allimage = database.Imagedata.query(database.Imagedata.streamId==str(stream.key.id())).fetch()
        #print(allimage)
        upload_url = blobstore.create_upload_url('/upload?')
        #print(upload_url)
        #print("{0}".format(upload_url))

        template_values = {
            'upload_url':"{0}".format(upload_url),
            'allimage':allimage,
            'stream':stream,
            'url': url,
            'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('Edit A Single Stream.html')
        #if(user==stream.user_id):
        #    template = JINJA_ENVIRONMENT.get_template('Edit A Single Stream.html')
        #else:
        #    template = JINJA_ENVIRONMENT.get_template('View A Single Stream.html')
        self.response.write(template.render(template_values))



'''
Action
'''
class DeleteStream(webapp2.RequestHandler):
    def post(self):
        try:
            user = users.get_current_user().user_id()
        except:
            return self.redirect("/")
        deleteList = self.request.get_all('delete')
        #for i in deleteList:
        #    print(i)
        #    if i in deleteList:
        #        print("!!!")
        #print(deleteList)
        deleteStreamQuery = database.Stream.query().fetch()
        for i in deleteStreamQuery:
            print(i.key.id())
            if(str(i.key.id()) in deleteList):
                i.key.delete()

        deleteImageQuery = database.Imagedata.query().fetch()
        for j in deleteImageQuery:
            if(j.streamId in deleteList):
                j.key.delete()
        self.redirect("/manage")

class UnsubscribeStream(webapp2.RequestHandler):
    def post(self):
        try:
            user = users.get_current_user.user_id()
        except:
            return self.redirect("/")
        unsubList = self.request.get_all('unsub')

        unsubStreamQuery = database.Stream.query(database.Stream.user_id==user).fetch()
        for i in unsubStreamQuery:
            if(i.stream_id in unsubList):
                i.key.delete()
        self.redirect("/manage")

class CreateStream(webapp2.RequestHandler):
    def post(self):
        try:
            user = users.get_current_user().user_id()
        except:
            return self.redirect("/")


        stream = database.Stream()#parent = ndb.Key('User', user))

        stream.userId = user
        stream.createTime = datetime.now()
        stream.lastTime = datetime.now()
        stream.tags = self.request.get_all('tag')
        stream.streamName = self.request.get('name')
        #print(self.request.get('name'))
        #print(self.request.get('coverImage'))
        stream.coverImageUrl = self.request.get('coverImage')
        stream.picNum = 0

        stream.put()

        self.redirect('/createstream')

        #own_stream = database.Stream.query(ndb.AND(database.Stream.user_id==user,database.Stream.create_time!=None)).order(-database.Stream.create_time).fetch()

        # listofsub=[]
        #for sss in own_stream:
        #    if sss.subscriber and sss.subscriber != 'Add subscriber emails':
        #        listofsub=sss.subscriber.split(",")
        #        for i in listofsub:
        #            mail.send_mail(sender="Miniproject :: Info <info@enhanced-oxygen-107815.appspotmail.com>",
        #            to=i,
        #            subject="Stream subscribe invitation",
        #            body="check out the stream at "+str(url))
class Upload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            user = users.get_current_user().user_id()
        except:
            return self.redirect("/")

        streamList = database.Stream.query().fetch()
        #print(streamList)
        for stream in streamList:
            if(stream.key.id()==self.request.get('streamId')):
                break

        upload = self.get_uploads()[0]

        #Store image data
        image = database.Imagedata()
        image.streamId = str(stream.key.id())
        image.userId = user
        image.comment = self.request.get('comments')
        image.url = images.get_serving_url(upload.key())
        image.name = self.request.get('filename')
        image.blobKey = upload.key()
        image.createTime = datetime.now()
        image.put()
        print(stream.picNum)
        stream.lastTime = image.createTime
        stream.picNum = int(stream.picNum) + 1
        stream.put()
        print(stream.picNum)
        #print(image)
        #print(stream)
        #template_values = {
        #   'image':image
        #}
        #template = JINJA_ENVIRONMENT.get_template('test.html')
        #self.response.write(template.render(template_values))
        self.redirect('/singlestream?curstream=%s' %self.request.get('stream_id'))



app = webapp2.WSGIApplication([
    ('/',LoginPage),
    ('/manage',ManagementPage),
    ('/delete',DeleteStream),
    ('/unsub',UnsubscribeStream),
    ('/createstream',CreateStreamPage),
    ('/create',CreateStream),
    ('/view',ViewAllPage),
    ('/singlestream',SingleStreamPage),
    ('/upload',Upload),
],debug=True)