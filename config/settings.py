import os
from pathlib import Path

# Побудова шляхів
BASE_DIR = Path(__file__).resolve().parent.parent

# ШВИДКЕ НАЛАШТУВАННЯ
SECRET_KEY = 'django-insecure-your-custom-secret-key-here'
DEBUG = True

ALLOWED_HOSTS = [
    'enda-unparenthesised-earnestine.ngrok-free.dev',
    '127.0.0.1',
    'localhost',
    '*'
]

# === 1. РЕЄСТРАЦІЯ ДОДАТКІВ ===
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'achievements',

    # --- Потрібно для Google входу (allauth) ---
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # -------------------------------------------

    'accounts',
    'news',
    'team',
    'matches',
    'pages',
    'gallery',
    'shop',

    'ckeditor',  # <--- ДОДАНО CKEDITOR
]

CSRF_TRUSTED_ORIGINS = [
    'https://enda-unparenthesised-earnestine.ngrok-free.dev',
    'http://enda-unparenthesised-earnestine.ngrok-free.dev',
]

SITE_ID = 1

# === 2. МIDDLEWARE ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'matches.context_processors.table_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# === 3. AUTHENTICATION_BACKENDS ===
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# === 4. НАЛАШТУВАННЯ ALLAUTH (ЛОГІКА ТА GOOGLE) ===
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'VERIFIED_EMAIL': True
    }
}

# Налаштування входу/реєстрації
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'account_login'

# Основна логіка акаунтів
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_UNIQUE_EMAIL = True

# Паролі (ПОВЕРТАЄМО ПРАВИЛЬНУ ФОРМУ)
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATE_ON_SIGNUP = True

# АВТОМАТИЧНЕ З'ЄДНАННЯ (ОДИН EMAIL = ОДИН АККАУНТ)
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True

# Емуляція пошти в консоль (щоб не було помилок)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / "static"]
else:
    STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "site_title": "Адмінка Покрова АМП",
    "site_header": "Покрова АМП",
    "site_brand": "ФК ПОКРОВА",
    "site_logo": "logo.png",
    "welcome_sign": "Вітаємо в панелі керування ФК Покрова АМП",
    "copyright": "ФК Покрова АМП",
    "search_model": ["auth.User", "news.Post"],
    "topmenu_links": [
        {"name": "Головна", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "На сайт", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["news", "matches", "pages", "auth"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "news.Post": "fas fa-newspaper",
        "matches.Match": "fas fa-futball",
        "matches.TournamentTable": "fas fa-table",
    },
}

JAZZMIN_UI_CONFIG = {
    "navbar_theme": "navbar-dark",
    "theme": "darkly",
    "accent": "accent-warning",
}

TELEGRAM_BOT_TOKEN = '8133559169:AAHVPNAknRmNL9rh5ZFQzWRLjH1MSBts0GM'
TELEGRAM_CHAT_ID = '1031408038'

# === НАЛАШТУВАННЯ ПАНЕЛІ РЕДАКТОРА (CKEDITOR) ===
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['RemoveFormat', 'Source']
        ],
        'height': 400,
        'width': '100%',
    }
}
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')