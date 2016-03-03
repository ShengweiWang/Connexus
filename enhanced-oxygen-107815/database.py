__author__ = 'sm'


from google.appengine.ext import ndb
from google.appengine.ext import blobstore


class Subscribe(ndb.Model):
    user_id = ndb.StringProperty()
    stream_id= ndb.StringProperty()
    user_email=ndb.StringProperty()

class trending(ndb.Model):
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

class frequency(ndb.Model):
     user_id = ndb.StringProperty()
     user_email=ndb.StringProperty()
     frequency = ndb.StringProperty()


class imagedata(ndb.Model):
     user_id = ndb.StringProperty()
     blob_key= ndb.BlobKeyProperty()
     comment = ndb.StringProperty()
     date = ndb.DateTimeProperty(auto_now_add=True)
     url = ndb.StringProperty()
     stream_id = ndb.StringProperty()
     name = ndb.StringProperty()
     position=ndb.StringProperty()

class stream(ndb.Model):
    user_id = ndb.StringProperty()
    user_email=ndb.StringProperty()
    owner=ndb.StringProperty()
    numberofpic = ndb.IntegerProperty()
    last_add = ndb.StringProperty()
    cover_key = ndb.BlobKeyProperty()  #ssss
    cover_url = ndb.StringProperty()  #ssss
    blob_key = ndb.BlobKeyProperty(repeated=True)
    tags =  ndb.StringProperty(repeated=True)
    stream_id = ndb.StringProperty()
    create_time = ndb.DateTimeProperty(auto_now_add=True)  #change
    invite_message = ndb.StringProperty()
    view = ndb.DateTimeProperty(repeated=True)
    numview = ndb.IntegerProperty()
    subscriber= ndb.StringProperty()
    view_in_hour = ndb.IntegerProperty()
