SETTINGS = {
    #First string in tuple is name of website, **must** be unique
    #Second string can be any URL, will be prefixed with http://
    'urls_to_check': (
        ('Example.com', 'www.example.com'),
    ),

    #These are used to check for connectivity to the internet
    'should_be_online': ('www.yahoo.com', 'www.google.com'),

    #URL to your appengine instance, used for linking in emails
    'appengine_url': 'example.appspot.com',

    #Pause duration when pausing notifications
    'pause_duration': 3600,

    #Both send and receive email for sendmail function, must be approved by appengine
    'email': 'gudbergur@example.com',

    #Boxcar user id and published id, get them both at boxcar.io
    'boxcar_user': 'gudbergur@example.com',
    'boxcar_publisher_id': '',

    #Set this to a timespan when it's sleepy time and a bit longer downtime
    #is not as critical. To disable make from and to same value.
    #Note that this is UTC time!
    #(0-23 hours, 0-59 minutes, 0-59 seconds)
    'sleeping_from': (0, 0, 0),
    'sleeping_to': (7, 0, 0),
}


