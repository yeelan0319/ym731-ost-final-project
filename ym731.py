import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor

import jinja2
import webapp2
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Question(ndb.Model):
    author = ndb.UserProperty(required=True)
    title = ndb.StringProperty(indexed=False, required=True)
    content = ndb.StringProperty(indexed=False, required=True)
    vote = ndb.IntegerProperty(default=0)
    ctime = ndb.DateTimeProperty(auto_now_add=True) #creation time
    utime = ndb.DateTimeProperty(auto_now=True) #update time

class Answer(ndb.Model):
    questionKey = ndb.KeyProperty(kind=Question)
    author = ndb.UserProperty(required=True)
    content = ndb.StringProperty(indexed=False, required=True)
    vote = ndb.IntegerProperty(default=0)
    ctime = ndb.DateTimeProperty(auto_now_add=True) #creation time
    utime = ndb.DateTimeProperty(auto_now=True) #update time

class MainHandler(webapp2.RequestHandler):
    def get(self):  #render main page
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
        else:
            url = users.create_login_url(self.request.uri)

        template_values = {
            'user': users.get_current_user(),
            'url': url,
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class QuestionsHandler(webapp2.RequestHandler):
    def get(self):  #fetch all questions by page
        curs = Cursor(urlsafe=self.request.get('cursor'))
        questions, next_curs, more = Question.query().order(-Question.utime).fetch_page(10, start_cursor=curs)

        template_values = {
            'questions': questions
        }
        template = JINJA_ENVIRONMENT.get_template('question.html')
        self.response.out.write(json.dumps({
            'status': 200,
            'data':{
                'content': template.render(template_values),
                'next_curs': next_curs.urlsafe(),
                'more': more
            }
        }));
    def post(self): #create new question
        question = Question(author=users.get_current_user(),
            title=self.request.get('title'),
            content=self.request.get('content')
        );
        questionKey = question.put()

        self.response.out.write(json.dumps({
            'status': 200,
            'data': {
                'qid': questionKey.urlsafe()
            }
        }));

class QuestionHandler(webapp2.RequestHandler):
    def get(self, qid):  #fetch single question
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
        else:
            url = users.create_login_url(self.request.uri)

        questionKey = ndb.Key(urlsafe=qid)
        question = questionKey.get()
        question.answers = Answer.query(Answer.questionKey == questionKey).order(-Answer.vote)

        template_values = {
            'user': users.get_current_user(),
            'url': url,
            'question': question
        }
        template = JINJA_ENVIRONMENT.get_template('detail.html')
        self.response.write(template.render(template_values))
    def post(self, qid):  #vote single question
        question = ndb.Key(urlsafe=qid).get()
        vote_type = self.request.get('type')
        if vote_type == "up":
            question.vote = question.vote + 1
        else: 
            question.vote = question.vote - 1
        question.put()

        self.response.out.write(json.dumps({
            'status': 200,
            'data': {
                'vote': question.vote
            }
        }));
    def put(self, qid):   #edit single question
        question = ndb.Key(urlsafe=qid).get()
        question.title = self.request.get('title')
        question.content = self.request.get('content')
        question.put()

        self.response.out.write(json.dumps({
            'status': 200,
            'data': {
            }
        }));
    def delete(self, qid):   #delete single question
        question = ndb.Key(urlsafe=qid).get()
        question.key.delete()
        self.response.out.write(json.dumps({
            'status': 200,
            'data': {
            }
        }));

class AnswersHandler(webapp2.RequestHandler):
    def post(self, qid): #create new answer
        questionKey = ndb.Key(urlsafe=qid)
        answer = Answer(questionKey=questionKey,
            author=users.get_current_user(),
            content=self.request.get('content')
        );
        answer.put()

        template_values = {
            'questionKey': questionKey,
            'answer': answer
        }
        template = JINJA_ENVIRONMENT.get_template('answer.html')
        self.response.out.write(json.dumps({
            'status': 200,
            'data': {
                'content': template.render(template_values)
            }
        })); 

class AnswerHandler(webapp2.RequestHandler):
    def post(self, qid, aid): #vote for answer
        answer = ndb.Key(urlsafe=aid).get()
        vote_type = self.request.get('type')
        if vote_type == "up":
            answer.vote = answer.vote + 1
        else: 
            answer.vote = answer.vote - 1
        answer.put()

        self.response.out.write(json.dumps({
            'status': 200,
            'data': {
                'vote': answer.vote
            }
        }));
    def put(self, qid, aid):  #edit answer
        answer = ndb.Key(urlsafe=aid).get()
        answer.content = self.request.get('content')
        answer.put()

        self.response.out.write(json.dumps({
            'status': 200,
            'data': {
            }
        }));
    def delete(self, qid, aid):  #delete answer
        answer = ndb.Key(urlsafe=aid).get()
        answer.key.delete()
        self.response.out.write(json.dumps({
            'status': 200,
            'data': {
            }
        }));

application = webapp2.WSGIApplication([
    (r'/', MainHandler),
    (r'/questions', QuestionsHandler),
    (r'/questions/([^/]+)?', QuestionHandler),
    (r'/questions/([^/]+)?/answers', AnswersHandler),
    (r'/questions/([^/]+)?/answers/([^/]+)?', AnswerHandler),
], debug=True)