Appnginpinger - Extremely basic pinger/web monitor meant to run on Google App Engine
=====

After www.wasitup.com was taken offline I needed a simple pinger/web monitor to watch my websites and notify me
if anything goes wrong. I think App Engine is a great no-maintenance platform to run a simple service like this.


Install
-----

Just move app.template.yaml to app.yaml and settings.template.py to settings.py and configure to suit you,
then deploy to App Engine via appcfg.py or Google App Engine Launcher.

Note that you must sign up for both user account and provider account with Boxcar (boxcar.io) to use the
push notification service.


Procedure
-----

Again, this project is so simple that if you're going to use it, just read the code.  But the procedure is this:
Cron (via cron.yaml) makes a request every minute to /check, which checks all URLs specified in SETTINGS
if they're online. If any of them is offline you get notified via email and Boxcar push notifications (iOS).

You can configure sleeping period, for e.g. if your websites are targeted at specific geographic area when
there's less stress when people are sleeping in which case the URLs must be offline for 10 consecutive
minutes before you're notified.

You can also pause notifications from all or specific hosts via /pause. As you must know the host md5 string
this is mainly meant for clicking in email notifications.


Settings
-----

**Better explained in settings.template.py**

urls_to_check is a tuple with tuples in the form of ("Name of Website", "http://www.example.com") 

should_be_online is a tuple with strings of sites that should be online, if all of them are offline we determine our App Engine instance to be offline.

email is a string with your email address which must be authorized to send email via App Engine.

boxcar_user and boxcar_publisher_id you get on boxcar.io by signing up for user account and provider account.

sleeping_from and sleeping_to are tuples with timespan when everyone is sleeping and a bit longer downtime is not as critical. I added this cause the websites I manage are mainly meant for a limited geographic area :)


