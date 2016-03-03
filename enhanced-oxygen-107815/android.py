import webapp2
from google.appengine.api import users, files, images
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import time
import json
import database

# class Image(ndb.Model):
#     blob_key = ndb.BlobKeyProperty()
#     dateCreated = ndb.DateTimeProperty(auto_now_add=True)
#     caption = ndb.StringProperty(indexed=False)

# class MainPage(webapp2.RequestHandler):
#     def get(self):
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.write('Hello, World!')

class GetUploadURL(webapp2.RequestHandler):
	def get(self):
		upload_url = blobstore.create_upload_url('/uploadHandler')
		upload_url = str(upload_url)
		dictPassed = {'upload_url':upload_url}
		jsonObj = json.dumps(dictPassed, sort_keys=True,indent=4, separators=(',', ': '))
		self.response.write(jsonObj)

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]
        urls= images.get_serving_url(upload.key())
        position="("+self.request.params['latitude']+"%"+self.request.params['longitude']+")"
        user_photo = database.imagedata(blob_key = upload.key(), stream_id=self.request.params['streamname'],comment=self.request.params['photoCaption'], url=urls,position=position)
        user_photo.put()
        stream=database.stream.query(database.stream.stream_id==self.request.params['streamname']).fetch()
        for i in stream:
            i.numberofpic+=1
            i.put()

class ViewAllPhotos(webapp2.RequestHandler):
    def get(self):
        user = self.request.get('user_id')
        allcover_query = database.stream.query(database.stream.create_time!=None).order(-database.stream.create_time)
        allcover = allcover_query.fetch()
        urllist=[]
        namelist=[]
        for i in allcover:
            urllist.append(i.cover_url)
            namelist.append(i.stream_id)

        position=[]
        imageurl=[]
        streamname=[]
        allimage_query = database.imagedata.query()
        allimage = allimage_query.fetch()
        for j in allimage:
            position.append(j.position)
            imageurl.append(j.url)
            streamname.append(j.stream_id)

        allsub_query=database.Subscribe.query(database.Subscribe.user_email==user).fetch()
        allsubstreamname=[]
        for i in allsub_query:
            allsubstreamname.append(i.stream_id)

        allsub=database.stream.query().fetch()

        suburl=[]
        subnamelist=[]
        for k in allsub:
            if k.stream_id in allsubstreamname:
                suburl.append(k.cover_url)
                subnamelist.append(k.stream_id)

        dictPassed={'displayImages':urllist, 'namelist':namelist, 'location':position, 'imageurl':imageurl, 'suburl':suburl, 'subnamelist':subnamelist, 'streamname':streamname}
        jsonObj=json.dumps(dictPassed,sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj)

class ViewSingle(webapp2.RequestHandler):
    def get(self):
        stream_name = self.request.get('stream_name')
        allimage_query = database.imagedata.query(ndb.AND(
            database.imagedata.stream_id == stream_name,database.imagedata.date!=None)).order(database.imagedata.date)
        allimage=allimage_query.fetch()

        imageURLList=[]
        captionlist=[]
        for pic in allimage:
            picURL = pic.url
            imageURLList.append(picURL)
            captionlist.append(pic.comment)

        dictPassed = {'displayImages':imageURLList, 'imageCaptionList':captionlist}
        jsonObj = json.dumps(dictPassed, sort_keys=True,indent=4, separators=(',', ': '))
        self.response.write(jsonObj)


app = webapp2.WSGIApplication([
    # ('/', MainPage),
    ('/getUploadURL',GetUploadURL),
    ('/uploadHandler', UploadHandler),
    ('/viewAllPhotos', ViewAllPhotos),
    ('/viewSingle', ViewSingle)
], debug=True)