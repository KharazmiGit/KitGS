import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if needed
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-j163*-0rhe7-hx!ct&9#u(iv6ygm!42zki^+z4d988+@p3kb+n'

DEBUG = True

ALLOWED_HOSTS = [
    '192.168.3.25',
    '127.0.0.1',
    '192.168.100.20',
    'localhost',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your apps
    'account.apps.AccountConfig',
    'scraper.apps.ScraperConfig',
    'core.apps.CoreConfig',
    'crispy_forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'account.custom_middleware.CustomMiddleware',
]

ROOT_URLCONF = 'KitGS.urls'

LOGIN_URL = '/accounts/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'KitGS.wsgi.application'

# ---------------- Database ----------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------- Password Validators ----------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------- Internationalization ----------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# ---------------- Static & Media ----------------
# Static files (CSS, JS, Fonts, Images)
STATIC_URL = '/static/'

# Where Django will look first (your custom static folder)
STATICFILES_DIRS = [
    BASE_DIR / "static",  # put your offline CSS/JS/fonts/images here
]

# Where `collectstatic` will copy everything (for production)
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media (user uploaded files, e.g. profile pics)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# ---------------- Default Auto Field ----------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------- Custom Keys ----------------
FERNET_KEY = 'NmobEP7hCP7-td0mkdZjtMLJX0y59MfALSLd-Al_aJ4='
# ---------------- the template pack ----------
CRISPY_TEMPLATE_PACK = 'bootstrap4'
