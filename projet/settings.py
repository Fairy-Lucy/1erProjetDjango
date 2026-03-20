SECRET_KEY = 'dev-key'

DEBUG = True

ALLOWED_HOSTS = []

ROOT_URLCONF = 'projet.urls'

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'main',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

STATIC_URL = 'static/'
