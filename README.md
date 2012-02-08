Appnginpinger
=====

**Extremely basic pinger/web monitor meant to run on Google App Engine**

After www.wasitup.com was taken offline I needed a simple pinger/web monitor to watch my websites and notify me
if anything goes wrong. I think App Engine is a great no-maintenance platform to setup and run a simple service like this.

Cron (via cron.yaml) makes a request every minute to /check, which checks all URLs specified in SETTINGS
if they're online. If any of them is offline you get notified via email and Boxcar push notifications.

Install
-----

Just move app.yaml.template to app.yaml and settings.py.template to settings.py and configure to suit you,
create a app on App Engine then deploy to App Engine via appcfg.py or Google App Engine Launcher.

This shouldn't be more than a 5 minute process.

Note that you must sign up for both user account and provider account with Boxcar (boxcar.io) to use the
push notification service.


Settings
-----

**Better explained in settings.template.py**

**urls_to_check** is a tuple with tuples in the form of ("Name of Website", "http://www.example.com") 

**should_be_online** is a tuple with strings of sites that should be online, if all of them are offline we determine our App Engine instance to be offline.

**email** is a string with your email address which must be authorized to send email via App Engine.

**secret_key**: You can pause notifications via /pause or resume via /resume. These URLs are protected via secret_key.

**pause_duration** indicates how long you want /pause to be

**appengine_url** is the url to your appspot instance

**boxcar_user and boxcar_publisher_id** you get on boxcar.io by signing up for user account and provider account.

**sleeping_from and sleeping_to**: You can configure sleeping period, for e.g. if your websites are targeted
at specific geographic area when there's less stress when people are sleeping in which case the URLs must be 
offline for 10 consecutive minutes before you're notified (you can disable this behavior).

