print("SETTINGS LOADED SUCCESSFULLY")

from pathlib import Path
import os
import sys
import logging
import dj_database_url   
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = [
    "dkexperience.com.ng",
    "www.dkexperience.com.ng",
    "dk-experiences.onrender.com",
    "dk-experiences",   # 👈 ADD THIS (VERY IMPORTANT)
    "localhost",
    "127.0.0.1"
]
CSRF_TRUSTED_ORIGINS = [
    'https://dk-experiences.onrender.com',
    'https://dkexperience.com.ng',
    'https://www.dkexperience.com.ng'
]

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'events',
    'core',
    'travel',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ ADD THIS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ PUT IT HERE (NOT inside middleware)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ROOT_URLCONF = 'dk_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dk_project.wsgi.application'
DATABASES = {
    'default': dj_database_url.parse('postgresql://dk_database_lwus_user:TCRCtWJzwlTvHtZTaVRflnOZ2yv5LxOp@dpg-d782cdtm5p6s73ehask0-a/dk_database_lwus')
}
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

PAYSTACK_PUBLIC_KEY = "pk_live_9275362cb1c7b8376e6ef21c4ee2bf944b9f9ecb"

logging.basicConfig(level=logging.DEBUG)


STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'