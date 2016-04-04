import logging

from google.appengine.api import mail
from google.appengine.api import taskqueue

from dateutil import *
from model import *

from django.conf import settings

from utilities import framework

REMINDER = """
Hey!

Your teammates want to know what you're up to. Don't leave 'em hanging.

Simply respond to this email with...
- highs and lows for last week
- plans for upcoming week
- any obstacles or challenges in your path

Feel free to link to wiki pages, designs, Google Docs or Github commits. Snippets are due by Monday at 7pm.

Hugs,
Snippets
"""


class ReminderEmail(framework.BaseHandler):
    def get(self):
        d = date_for_retrieval()
        all_users = User.all().filter("enabled =", True).fetch(500)
        
        for user in all_users:
            if user.email in submitted_users(d):
                logging.info("Submitted: " + user.email) 
            else:
                taskqueue.add(url='/onereminder', params={
                    'email': user.email,
                    'final': self.request.get('final')
                    })

class OneReminderEmail(framework.BaseHandler):
    def post(self):
        body = REMINDER
        subject = "Snippet time!"
        if self.request.get('final') == "true":
            subject = "Re: " + subject 
            body = "Just a heads up, your snippets are due by 7pm today."
        
        logging.info(self.request.get('email'))
        logging.info(subject)
        logging.info(body)
        #mail.send_mail(sender="Snippets <" + settings.SITE_EMAIL + ">",
        #               to=self.request.get('email'),
        #               subject=subject,
        #               body=body)

    def get(self):
        self.post()


class DigestEmail(framework.BaseHandler):
    def get(self):
        all_users = User.all().filter("enabled =", True).fetch(500)
        for user in all_users:
            taskqueue.add(url='/onedigest', params={'email': user.email})


class OneDigestEmail(framework.BaseHandler):
    def __send_mail(self, recipient, body):
        mail.send_mail(sender="Snippets <" + settings.SITE_EMAIL + ">",
                       to=recipient,
                       subject="Snippet delivery!",
                       body=body)

    def __snippet_to_text(self, snippet):
        divider = '-' * 30
        return '%s\n%s\n%s' % (snippet.user.pretty_name(), divider, snippet.text)

    def get(self):
        self.post()

    def post(self):
        user = user_from_email(self.request.get('email'))
        d = date_for_retrieval()
        all_snippets = Snippet.all().filter("date =", d).fetch(500)
        all_users = User.all().fetch(500)
        following = compute_following(user, all_users)
        logging.info(all_snippets)
        body = '\n\n\n'.join([self.__snippet_to_text(s) for s in all_snippets if s.user.email in following])
        if body:
            self.__send_mail(user.email, 'https://' + settings.SITE_DOMAIN + '\n\n' + body)
        else:
            logging.info(user.email + ' not following anybody.')
