#!/usr/bin/env python

import urllib
import time
import logging
import hashlib
import datetime

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
from google.appengine.api import mail
from google.appengine.api import memcache

from settings import SETTINGS

def boxcar(message, title=None, url_tuple=None):
    urlname_md5 = (hashlib.md5(url_tuple[0]).hexdigest(),)
    if memcache.get(nonotify_key(urlname_md5)) or memcache.get(nonotify_key()):
        return False

    if not title:
        title = "%s : %s" % (url_tuple[0], message)

    url = "http://boxcar.io/devices/providers/%s/notifications" % (SETTINGS['boxcar_publisher_id'],)
    form_fields = {
        "email": SETTINGS['boxcar_user'],
        "notification[from_screen_name]": title,
        "notification[message]": message
    }
    form_data = urllib.urlencode(form_fields)
    result = urlfetch.fetch(url=url,
                            payload=form_data,
                            method=urlfetch.POST,
                            headers={'Content-Type': 'application/x-www-form-urlencoded'})
    return result.status_code == 200

def sendmail(message, title=None, url_tuple=None):
    urlname_md5 = (hashlib.md5(url_tuple[0]).hexdigest(),)
    if memcache.get(nonotify_key(urlname_md5)) or memcache.get(nonotify_key()):
        return False

    if not title:
        title = "%s : %s" % (url_tuple[0], message)

    message += """\n
http://%s/pause
http://%s/pause?urlname_md5=%s
http://%s/resume
http://%s/resume?urlname_md5=%s""" % (
        SETTINGS['appengine_url'],
        SETTINGS['appengine_url'],
        nonotify_key,
        SETTINGS['appengine_url'],
        SETTINGS['appengine_url'],
        nonotify_key)
    sent = mail.send_mail(sender=SETTINGS['email'],
                  to=SETTINGS['email'],
                  subject=title,
                  body=message)
    return sent

def notify(message, title=None, url_tuple=None):
    boxcar(message, title, url_tuple)
    sendmail(message, title, url_tuple)

def site_up(url):
    url = "http://%s" % url
    try:
        result = urlfetch.fetch(url)
    except urlfetch.DownloadError, e:
        logging.error(e)
        return False
    return result.status_code == 200

def is_connected():
    for host in SETTINGS['should_be_online']:
        if site_up(host):
            return True
    return False

def is_sleeping():
    now_tuple = tuple(getattr(datetime.datetime.now(), x) for x in ['hour', 'minute', 'second'])
    return SETTINGS['sleeping_from'] < now_tuple and now_tuple < SETTINGS['sleeping_to']

def check_site(url_tuple):
    down_key = "down_%s" % (hashlib.md5(url_tuple[0]).hexdigest(),)
    was_down = memcache.get(down_key)
    is_up = site_up(url_tuple[1])
    if is_up:
        if was_down:
            sendmail("Ok, it's back up :)", url_tuple=url_tuple)
            memcache.delete(down_key)
            return "back up"
        else:
            return "is up"
    else:
        if was_down:
            notification_list = [1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 50, 60, 90, 120]
            if is_sleeping():
                notification_list = filter(lambda x: x >= 10, notification_list)
            if was_down in notification_list:
                notify("STILL DOWN!", url_tuple=url_tuple)
            memcache.incr(down_key)
            return "still down"
        else:
            time.sleep(10)
            if is_connected() and not site_up(url_tuple[1]):
                if not is_sleeping():
                    notify("JUST WENT DOWN!", url_tuple=url_tuple)
                memcache.add(key=down_key, value=1, time=86400)
                return "went down"
            else:
                return "is up, responded to 2nd request"

def check_all():
    output = ""
    if not is_connected():
        logging.error("not connected")
        return "not connected"
    for url_tuple in SETTINGS['urls_to_check']:
        output += "%s: %s \n" % (url_tuple[0], check_site(url_tuple),)
    logging.info(output)
    return output

def nonotify_key(urlname_md5=None):
    return "nonotify_%s" % (urlname_md5,) if urlname_md5 else "nonotify"

def pause(urlname_md5=None):
    memcache.add(key=nonotify_key(urlname_md5), value=True, time=SETTINGS['pause_duration'])
    return "OK"

def resume(urlname_md5=None):
    memcache.delete(nonotify_key(urlname_md5))
    return "OK"

class PauseHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(pause(self.request.get("urlname_md5", None)))

class ResumeHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(resume(self.request.get("urlname_md5", None)))

class CheckHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(check_all())

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Very simple ping service on Google App Engine')

def main():
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/check', CheckHandler),
        ('/pause', PauseHandler),
        ('/resume', ResumeHandler)
        ], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()