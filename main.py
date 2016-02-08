#!/usr/bin/env python

import sys
import os

sys.path.append(os.path.join(os.path.abspath('.'), 'venv/lib/python2.7/site-packages'))

import telegram
import webapp2
import json

token='<Your_Token>'
bot = telegram.Bot(token)


class DeployedHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Deployed')


class HookHandler(webapp2.RequestHandler):
    def post(self):
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(json.loads(self.request.body))

        chat_id = update.message.chat.id

        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.message.text.encode('utf-8')

        # repeat the same message back (echo)
        bot.sendMessage(chat_id=chat_id, text=text)


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        s = bot.setWebhook('https://telegrambot-parrot.appspot.com/'+token)
        if s:
            self.response.write('webhook setup ok')
        else:
            self.response.write('webhook setup failed')


app = webapp2.WSGIApplication([
    ('/', DeployedHandler),
    ('/'+token, HookHandler),
    ('/set_webhook', SetWebhookHandler)
], debug=True)
