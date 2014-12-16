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

class Answer(ndb.Model):
    author = ndb.UserProperty(required=True)
    content = ndb.StringProperty(indexed=False, required=True)
    vote = ndb.IntegerProperty(default=0)
    ctime = ndb.DateTimeProperty(auto_now_add=True) #creation time
    utime = ndb.DateTimeProperty(auto_now=True) #update time

class Question(ndb.Model):
    author = ndb.UserProperty(required=True)
    title = ndb.StringProperty(indexed=False, required=True)
    content = ndb.StringProperty(indexed=False, required=True)
    vote = ndb.IntegerProperty(default=0)
    ctime = ndb.DateTimeProperty(auto_now_add=True) #creation time
    utime = ndb.DateTimeProperty(auto_now=True) #update time
    answers = ndb.StructuredProperty(Answer, repeated=True)

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

# class QuestionHandler(webapp2.RequestHandler):
#     def post(self):

#         # We set the same parent key on the 'Greeting' to ensure each Greeting
#         # is in the same entity group. Queries across the single entity group
#         # will be consistent. However, the write rate to a single entity group
#         # should be limited to ~1/second.
#         guestbook_name = self.request.get('guestbook_name',
#                                           DEFAULT_GUESTBOOK_NAME)
#         greeting = Greeting(parent=guestbook_key(guestbook_name))

#         if users.get_current_user():
#             greeting.author = users.get_current_user()

#         greeting.content = self.request.get('content')
#         greeting.put()

#         query_params = {'guestbook_name': guestbook_name}
#         self.redirect('/?' + urllib.urlencode(query_params))
#     def get(self):
#         qid = self.request.get('qid')

class ListHandler(webapp2.RequestHandler):
    def get(self):  #fetch all questions
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')
#     def post(self): #create new question

class QuestionHandler(webapp2.RequestHandler):
    def get(self, qid):  #fetch single question
        self.response.write('This is the ProductHandler. '
            'The product id is %s' % qid)
#     def post(self, qid):  #vote single question
#     def put(self, qid):   #edit single question
#     def delete(self, qid):   #delete single question

class AnswerHandler(webapp2.RequestHandler):
    def get(self, qid, aid):
        self.response.write('This is the ProductHandler. '
            'The product id is %s' % aid)
#     def post(self, qid, aid): #vote for answer
#     def put(self, qid, aid):  #edit answer
#     def delete(self, qid, aid):  #delete answer


application = webapp2.WSGIApplication([
    (r'/', ListHandler),
    (r'/questions', ListHandler),
    (r'/questions/(\d+)', QuestionHandler),
    (r'/questions/(\d+)/answers/(\d+)', AnswerHandler),
], debug=True)