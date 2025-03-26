from notaminfo.settings.dev import *
#  settings for docker in development

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'saved_notams',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST':'db',
        'PORT':'3306',
    }
}

CELERY_BROKER_URL = 'redis://redis:6379/1'  # Redis URL