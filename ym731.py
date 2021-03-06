import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor

import jinja2
import webapp2
import json
import re
import time

BASEURL = "http://hao-question.appspot.com"

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def contentParser(content):
    content = re.sub(r'(http[s]?://)([^\s]*)','<a target="_blank" href="\\1\\2">\\1\\2</a>',content)
    content = re.sub(r'<a target="_blank" href="(http[s]?://[^\s]*[(.jpg)(.png)(.gif)])">.*</a>', '<img src="\\1" height="300">', content)
    content = content.replace('\n', '<br/>')
    return content

class Question(ndb.Model):
    author = ndb.UserProperty(required=True)
    title = ndb.StringProperty(indexed=False, required=True)
    content = ndb.StringProperty(indexed=False, required=True)
    vote = ndb.IntegerProperty(default=0)
    ctime = ndb.DateTimeProperty(auto_now_add=True) #creation time
    utime = ndb.DateTimeProperty(auto_now=True) #update time
    tags = ndb.JsonProperty()

class Answer(ndb.Model):
    questionKey = ndb.KeyProperty(kind=Question)
    author = ndb.UserProperty(required=True)
    content = ndb.StringProperty(indexed=False, required=True)
    vote = ndb.IntegerProperty(default=0)
    ctime = ndb.DateTimeProperty(auto_now_add=True) #creation time
    utime = ndb.DateTimeProperty(auto_now=True) #update time

class Image(ndb.Model):
    ifile = ndb.BlobProperty()
    url = ndb.StringProperty()
    user = ndb.UserProperty(required=True)
    ctime = ndb.DateTimeProperty(auto_now_add=True)

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
        if users.get_current_user():
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
        else:
            self.response.out.write(json.dumps({
                'status': 403,
                'data': {
                    'message': 'Please login to vote'
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
        question.content = contentParser(question.content)

        answers = Answer.query(Answer.questionKey == questionKey).order(-Answer.vote)
        for answer in answers :
            answer.content = contentParser(answer.content)
        question.answers = answers

        template_values = {
            'user': users.get_current_user(),
            'url': url,
            'question': question
        }
        template = JINJA_ENVIRONMENT.get_template('detail.html')
        self.response.write(template.render(template_values))
    def post(self, qid):  #vote single question
        if users.get_current_user():
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
        else:
            self.response.out.write(json.dumps({
                'status': 403,
                'data': {
                    'message': 'Please login to vote'
                }
            }));
    def put(self, qid):   #edit single question
        question = ndb.Key(urlsafe=qid).get()
        editType = self.request.get("type")
        if editType == "tag":
            question.tags = self.request.get("tag")
            question.put()
            self.response.out.write(json.dumps({
                'status': 200,
                'data': {
                    'content': contentParser(question.content)
                }
            }));
        elif editType == "content":
            if users.get_current_user() == question.author:
                question.title = self.request.get('title')
                question.content = self.request.get('content')
                question.put()
                self.response.out.write(json.dumps({
                    'status': 200,
                    'data': {
                        'content': contentParser(question.content)
                    }
                }));
            else:
                self.response.out.write(json.dumps({
                    'status': 401,
                    'data': {
                        'message': 'You do not have the authority to edit this question'
                    }
                }));

    def delete(self, qid):   #delete single question
        question = ndb.Key(urlsafe=qid).get()
        if users.get_current_user() == question.author:
            question.key.delete()
            self.response.out.write(json.dumps({
                'status': 200,
                'data': {
                }
            }));
        else:
            self.response.out.write(json.dumps({
                'status': 401,
                'data': {
                    'message': 'You do not have the authority to delete this question'
                }
            }));

class RssHandler(webapp2.RequestHandler):
    def get(self, qid):
        questionKey = ndb.Key(urlsafe=qid)
        question = questionKey.get()
        question.content = question.content

        answers = Answer.query(Answer.questionKey == questionKey).order(-Answer.vote)
        for answer in answers :
            answer.content = answer.content
        question.answers = answers

        template_value = {
            'question' : question,
        }
        self.response.headers['Content-Type'] = 'text/xml'
        template = JINJA_ENVIRONMENT.get_template('rss.xml')
        self.response.write(template.render(template_value))

class AnswersHandler(webapp2.RequestHandler):
    def post(self, qid): #create new answer
        if users.get_current_user():
            questionKey = ndb.Key(urlsafe=qid)
            answer = Answer(questionKey=questionKey,
                author=users.get_current_user(),
                content=self.request.get('content')
            );
            answer.put()

            answer.content = contentParser(answer.content)
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
        else:
            self.response.out.write(json.dumps({
                'status': 403,
                'data': {
                    'message': 'Please login to answer'
                }
            }));

class AnswerHandler(webapp2.RequestHandler):
    def post(self, qid, aid): #vote for answer
        if users.get_current_user():
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
        else:
            self.response.out.write(json.dumps({
                'status': 403,
                'data': {
                    'message': 'Please login to vote'
                }
            }));
    def put(self, qid, aid):  #edit answer
        answer = ndb.Key(urlsafe=aid).get()
        if users.get_current_user() == answer.author:
            answer.content = self.request.get('content')
            answer.put()

            self.response.out.write(json.dumps({
                'status': 200,
                'data': {
                    'content': contentParser(answer.content)
                }
            }));
        else:
            self.response.out.write(json.dumps({
                'status': 401,
                'data': {
                    'message': 'You do not have the authority to edit this answer'
                }
            }));
    def delete(self, qid, aid):  #delete answer
        answer = ndb.Key(urlsafe=aid).get()
        if users.get_current_user() == answer.author:
            answer.key.delete()
            self.response.out.write(json.dumps({
                'status': 200,
                'data': {
                }
            }));
        else:
            self.response.out.write(json.dumps({
                'status': 401,
                'data': {
                    'message': 'You do not have the authority to delete this answer'
                }
            }));

class ImagesHandler(webapp2.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
        else:
            url = users.create_login_url(self.request.uri)
        images = Image.query(Image.user==users.get_current_user()).order(-Image.ctime)
        template_values = {
            'user': users.get_current_user(),
            'url': url,
            'images': images,
            'baseUrl': BASEURL
        }
        template = JINJA_ENVIRONMENT.get_template('images.html')
        self.response.write(template.render(template_values))
    def post(self):
        if users.get_current_user():
            image = Image()
            image.ifile = self.request.get('img')
            image.user = users.get_current_user()
            image.put()
            time.sleep(1)
            self.redirect('/images')

class ImageHandler(webapp2.RequestHandler):
    def get(self, iid):
        image = ndb.Key(urlsafe=iid).get()
        self.response.headers['content-Type'] = 'image/png'
        self.response.write(image.ifile)

application = webapp2.WSGIApplication([
    (r'/', MainHandler),
    (r'/images', ImagesHandler),
    (r'/images/([^/]+)?', ImageHandler),
    (r'/questions', QuestionsHandler),
    (r'/questions/([^/]+)?', QuestionHandler),
    (r'/questions/([^/]+)?/rss', RssHandler),
    (r'/questions/([^/]+)?/answers', AnswersHandler),
    (r'/questions/([^/]+)?/answers/([^/]+)?', AnswerHandler),
], debug=True)