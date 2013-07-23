from basesettings import *

# This is an example of settings that could be overridden. You can
# override more, but these are probably the ones you want to start
# with.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('bmistree', 'bmistree@gmail.com'),
)
MANAGERS = ADMINS


DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

# use existing default database name
# DATABASES['default']['NAME'] = 'sessions.db'

# Make this unique, and don't share it with anybody. You MUST change this.
SECRET_KEY = '%5=mrbqodk6q-f+y-4m5r-&uryq(t*hpfkfa1fqmamq8!ydhm-'

