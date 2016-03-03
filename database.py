__author__ = 'sm'


from google.appengine.ext import ndb
from google.appengine.ext import blobstore


class Subscribe(ndb.Model):
    user_id = ndb.StringProperty()
    stream_id= ndb.StringProperty()
    user_email=ndb.StringProperty()

class Trending(ndb.Model):
    top_id=ndb.StringProperty(repeated=True)
    top_view=ndb.IntegerProperty(repeated=True)

class User(ndb.Model):
    """Sub model for representing an author."""
    user_id = ndb.StringProperty()
    email = ndb.StringProperty()
    subscribe = ndb.StringProperty(repeated=True)
    own = ndb.StringProperty(repeated=True)

    def add_stream(self, new_stream):
        if new_stream.stream_id in self.own:
            return
        else:
            self.own.insert(0, new_stream.stream_id)
        self.put()
        new_stream.put()

    def sub_stream(self, new_stream):
        if new_stream.stream_id in self.subscribe:
            return
        else:
            self.subscribe.insert(0, new_stream.stream_id)
        self.put()
        new_stream.put()

class Frequency(ndb.Model):
     user_id = ndb.StringProperty()
     user_email=ndb.StringProperty()
     frequency = ndb.StringProperty()


class Imagedata(ndb.Model):
     name = ndb.StringProperty()   #name for image
     blobKey = ndb.BlobKeyProperty() #blob key store
     comment = ndb.StringProperty()
     createTime = ndb.DateTimeProperty(auto_now_add=True)
     url = ndb.StringProperty()   #url, src=...
     userId = ndb.StringProperty()  #userid, key
     streamId = ndb.StringProperty()  #streamid, key
     #position=ndb.StringProperty()

class Stream(ndb.Model):
    streamName = ndb.StringProperty() #stream name
    userId = ndb.StringProperty()
    createTime = ndb.DateTimeProperty(auto_now_add=True)  #created timoe
    lastTime = ndb.DateTimeProperty(auto_now_add=True)
    tags = ndb.StringProperty(repeated=True)
    picNum = ndb.IntegerProperty()
    coverImageUrl = ndb.StringProperty()
    #user_email = ndb.StringProperty()
    #owner=ndb.StringProperty()


    #last_add = ndb.StringProperty()
    #cover_key = ndb.BlobKeyProperty()  #ssss
    #cover_url = ndb.StringProperty()  #ssss
    #blob_key = ndb.BlobKeyProperty(repeated=True)



    #invite_message = ndb.StringProperty()
    #view = ndb.DateTimeProperty(repeated=True)
    #numview = ndb.IntegerProperty()
    #subscriber= ndb.StringProperty()
    #view_in_hour = ndb.IntegerProperty()
