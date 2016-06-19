import json

from google.appengine.api import urlfetch
from google.appengine.ext import deferred

from django.conf import settings

class MandrillEmail(object):

    @classmethod
    def email(
        cls, email, recipient_name, subject, tags, message_text, message_html
    ):
        message = {
            'from_email': settings.FROM_EMAIL,
            'from_name': settings.FROM_NAME,
            'html': message_html,
            'subject': subject,
            'tags': tags,
            'text': message_text,
            'to': [{
                'email': email,
                'name': recipient_name,
                'type': 'to'
            }],
            'headers': {
                'Reply-To': settings.SITE_EMAIL
            },
        }

        deferred.defer(
            cls.send,
            message,
            _queue='emails',
        )

    @classmethod
    def send(cls, message):
        message = {
            'key': settings.MANDRILL_API_KEY,
            'message': message
        }

        urlfetch.fetch(
            url='https://mandrillapp.com/api/1.0/messages/send.json',
            payload=json.dumps(message),
            method=urlfetch.POST,
            headers={
                'Content-Type': 'Content-type: application/json; charset=utf-8'
            }
        )