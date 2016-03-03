import os
import urllib
import singlestream
import Viewall
import Search
import database
import singlestream
import json

from google.appengine.api import mail
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

# Default_owner_name = 'Anonymous'

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

Default_owner_name = 'Anonymous'
def owner_key(owner_name=Default_owner_name):
    """Constructs a Datastore key for a Guestbook entity.
    We use guestbook_name as the key.
    """
    return ndb.Key('owners', owner_name)

class Create(webapp2.RequestHandler):
    def get(self):
        # guestbook_name = self.request.get('guestbook_name',
        #                                   DEFAULT_GUESTBOOK_NAME)
        try:
            user = users.get_current_user().user_id()
        except:
            return self.redirect("/")

        sname=[]
        astream=database.stream.query().fetch()
        for s in astream:
            sname.append(s.stream_id)
        strname=json.dumps(sname)

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
            'streamnames':strname,
            # 'guestbook_name':guestbook_name
        }

        template = JINJA_ENVIRONMENT.get_template('create.html')
        self.response.write(template.render(template_values))


class CreateStream(webapp2.RequestHandler):
    def post(self):


        user = users.get_current_user().user_id()
        streaming = database.stream.query(database.stream.stream_id!=None).fetch()

        for i in streaming:
            if (i.stream_id == self.request.get('name')):
                return self.redirect('/error')

        if (self.request.get('name')==""):
            return self.redirect('/error3')

        stream = database.stream(parent = ndb.Key('User', user))
        stream.numberofpic = 0
        stream.user_id = user
        last_add = str(datetime.now())
        stream.last_add=last_add[:19]
        stream.create_time=datetime.now()
        stream.numview=0
        stream.stream_id = self.request.get('name')
        stream.invite_message = self.request.get('invite_message')

        direct = {'stream_name': self.request.get('name')}
        direct = urllib.urlencode(direct)
        url="http://enhanced-oxygen-107815.appspot.com/singlestream?"+ direct

        if self.request.get('subscriber'):
            stream.subscriber = self.request.get('subscriber')


        tags=self.request.get('tag')
        tags.split(",")
        for i in tags:
            stream.tag.append(i)

        if self.request.get('cover_image'):
            stream.cover_url = self.request.get('cover_image')
        else:
            stream.cover_url = "http://lh3.googleusercontent.com/aHVWqx3TgwzGTX4LfSnybFl7MAdq5JnaeP7xA0yzXrzNxgp4P9FOENxfahpNJ6RJ3up5f9fkncmQaOHdIL1xr0AXWwtuk5SZKIaETg"
        stream.owner = user
        stream.put()


        own_stream = database.stream.query(ndb.AND(database.stream.user_id==user,database.stream.create_time!=None)).order(-database.stream.create_time).fetch()

        # listofsub=[]
        for sss in own_stream:
            if sss.subscriber and sss.subscriber != 'Add subscriber emails':
                listofsub=sss.subscriber.split(",")
                for i in listofsub:
                    mail.send_mail(sender="Miniproject :: Info <info@enhanced-oxygen-107815.appspotmail.com>",
                    to=i,
                    subject="Stream subscribe invitation",
                    body="check out the stream at "+str(url))



        # for sub in listofsub:
        #     mail.send_mail(sender="Project Name :: Info <info@enhanced-oxygen-107815.appspotmail.com>",
        #     to=str(sub),
        #     subject="Stream subscribe invitation",
        #     body="check out the stream at "+str(url))
        # mail.send_mail(sender="Project Name :: Info <info@enhanced-oxygen-107815.appspotmail.com>",
        # to=str(stream.subscriber),
        # subject="Stream subscribe invitation",
        # body="check out the stream at "+str(url))


        self.redirect('/manage')

app = webapp2.WSGIApplication([
    ('/createstreamsign', CreateStream),
    ('/createstream', Create)
        ], debug=True)


