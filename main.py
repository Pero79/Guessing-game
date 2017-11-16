#!/usr/bin/env python

import os
import jinja2
import webapp2
import random


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

    def post(self):
        secret = 23
        guess = int(self.request.get("guess"))
        message = ""
        ponovi = ""

        if guess >= 1 and guess <= 30:
            if guess == secret:
             message = ("You guessed the lucky number  "+str(secret)+"  Congratulations!!!")
            else:
             ponovi = "To bad you didn't guess the luckey number ... Number  "+str(guess)+"  is not the lucky number. More luck next time!!!"

        params = {"message": message, "ponovi": ponovi}

        return self.render_template("random.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
