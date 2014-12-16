import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)

class Greeting(ndb.Model):
    """Models an individual Guestbook entry."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class Question(object):
    """__init__() functions as the class constructor"""
    def __init__(self, qid=None, title=None, content=None, answerno=None, author=None, utime=None, answers=None, vote=0):
        self.qid = qid
        self.title = title
        self.content = content
        self.answerno = answerno
        self.author = author
        self.utime = utime
        self.answers = answers
        self.vote = vote

class Answer(object):
    """__init__() functions as the class constructor"""
    def __init__(self, aid=None, qid=None, content=None, author=None, utime=None, vote=0):
        self.aid = aid
        self.qid = qid
        self.content = content
        self.author = author
        self.utime = utime
        self.vote = vote

class MainPage(webapp2.RequestHandler):

    def get(self):
        # guestbook_name = self.request.get('guestbook_name',
        #                                   DEFAULT_GUESTBOOK_NAME)
        # greetings_query = Greeting.query(
        #     ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        # greetings = greetings_query.fetch(10)

        questions = []
        questions.append(Question(1, "What's up Z!!!!","Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo. Quisque sit amet est et sapien ullamcorper pharetra. Vestibulum erat ", 8, "Yiran Mao", "Dec-15 22:26"));
        questions.append(Question(2, "What's up Z!!!!","Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo. Quisque sit amet est et sapien ullamcorper pharetra. Vestibulum erat ", 11, "Zihang Li", "Dec-15 22:33"));
        questions[0].contentpreview = questions[0].content
        questions[1].contentpreview = questions[1].content

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
        else:
            url = users.create_login_url(self.request.uri)

        template_values = {
            'questions': questions,
            'user': users.get_current_user(),
            'url': url,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
        
class DetailPage(webapp2.RequestHandler):

    def get(self):
        answers = []
        answers.append(Answer(1, 1, "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo. Quisque sit amet est et sapien ullamcorper pharetra. Vestibulum erat ", "Yiran Mao", "Dec-15 22:26"));
        answers.append(Answer(2, 1, "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo. Quisque sit amet est et sapien ullamcorper pharetra. Vestibulum erat ", "Zihang Li", "Dec-15 22:33"));
        
        question = Question(1, "What's up Z!!!!","Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo. Quisque sit amet est et sapien ullamcorper pharetra. Vestibulum erat ", 8, "Yiran Mao", "Dec-15 22:26", answers);
        
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
        else:
            url = users.create_login_url(self.request.uri)

        template_values = {
            'question': question,
            'user': users.get_current_user(),
            'url': url,
        }

        template = JINJA_ENVIRONMENT.get_template('detail.html')
        self.response.write(template.render(template_values))

class Guestbook(webapp2.RequestHandler):
    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/detail', DetailPage),
    ('/sign', Guestbook),
], debug=True)