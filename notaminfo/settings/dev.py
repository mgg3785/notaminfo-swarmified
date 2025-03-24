from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-82x2f8ej7cwkf!*#ovw9t198y^fjz*f+mq_fd&cdkh!wj(dn70'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'saved_notams',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST':'localhost',
        'PORT':'3306',
    }
}