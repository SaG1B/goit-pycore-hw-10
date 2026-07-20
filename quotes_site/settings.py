import os
from pathlib import Path

# Побудова шляхів всередині проєкту (наприклад: BASE_DIR / 'subdir')
BASE_DIR = Path(__file__).resolve().parent.parent

# Швидкі налаштування для розробки (не підходить для production!)
SECRET_KEY = 'django-insecure-your-secret-key-change-this-in-production'

DEBUG = True

ALLOWED_HOSTS = []


# Реєстрація додатків
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Твої власні додатки
    'quotes',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'quotes_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Шукаємо шаблони спочатку в папці templates на рівні проєкту, а потім всередині додатків
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'quotes_site.wsgi.application'


# Тимчасово підключаємо просту базу SQLite, щоб усе працювало без Docker/Postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Валідація паролів
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Мова та часовий пояс
LANGUAGE_CODE = 'uk-ua'

TIME_ZONE = 'Europe/Kyiv'

USE_I18N = True

USE_TZ = True


# Статичні файли (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Автоматичне поле для первинних ключів (ID)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Налаштування перенаправлення для авторизації
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'quotes:root'
LOGOUT_REDIRECT_URL = 'quotes:root'