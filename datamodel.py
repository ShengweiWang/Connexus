from google.appengine.ext import ndb

class User(ndb.Model):
    """ Model for representing an user"""
    id=ndb.StringProperty()
    email=ndb.StringProperty()
    subscribe=ndb.StringProperty(repeated=True)
    own=ndb.StringProperty(repeated=True)


class Stream(ndb.Model):
    """ Model for representing a stream"""
    id=ndb.StringProperty()
    imgids=ndb.StringProperty(repeated=True)
    date = ndb.DateTimeProperty(auto_now_add=True)


class Image(ndb.Model):
    """ Model for representing an image"""
    id=ndb.StringProperty()
    img=ndb.BlobProperty()
    comment = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    name=ndb.StringProperty()


