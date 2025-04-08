import os
from .base import *
from config.env import env

DEBUG = env.bool('DJANGO_DEBUG', default=False)

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])