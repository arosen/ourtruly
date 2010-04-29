import os
from google.appengine.ext.webapp import template

import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    toaddress = db.StringProperty(multiline=True)
    toaddress1 = db.StringProperty(multiline=True)
    tocity = db.StringProperty(multiline=False)
    tostate = db.StringProperty(multiline=False)
    tozip = db.StringProperty(multiline=False)
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
	    def get(self):
	        greetings_query = Greeting.all().order('-date')
	        greetings = greetings_query.fetch(10)

	        if users.get_current_user():
	            url = users.create_logout_url(self.request.uri)
	            url_linktext = 'Logout'
	        else:
	            url = users.create_login_url(self.request.uri)
	            url_linktext = 'Login'

	        template_values = {
	            'greetings': greetings,
	            'url': url,
	            'url_linktext': url_linktext,
	            }

	        path = os.path.join(os.path.dirname(__file__), 'index.html')
	        self.response.out.write(template.render(path, template_values))

class Confirm(webapp.RequestHandler):
    def post(self):
        greeting = Greeting()
        greeting.content = self.request.get('content')
        greeting.toaddress = self.request.get('toaddress')
        greeting.toaddress1 = self.request.get('toaddress1')
        greeting.tocity = self.request.get('tocity')
        greeting.tostate = self.request.get('tostate')
        greeting.tozip = self.request.get('tozip')

        greeting.put()

        content_values = {
            'greeting_content': greeting.content,
            'greeting_toaddress': greeting.toaddress,
            'greeting_toaddress1': greeting.toaddress1,
            'greeting_tocity': greeting.tocity,
            'greeting_tostate': greeting.tostate,
            'greeting_tozip': greeting.tozip,
        }

        path = os.path.join(os.path.dirname(__file__), 'confirm.html')
        self.response.out.write(template.render(path, content_values))


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/confirm', Confirm)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()