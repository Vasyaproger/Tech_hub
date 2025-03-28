"""
Django settings for backend project.
Generated by 'django-admin startproject' using Django 4.2.
For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%x&kg-nx75kirv^12#m@y0f486)4bphas#&6-m224qr%4iv$2o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'  # По умолчанию True для разработки

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'vh438.timeweb.ru', 'boodaikg.com']  # Добавлены хосты для продакшена

# Application definition
INSTALLED_APPS = [
    'admin_interface',  # Перед django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'shop',
    'corsheaders',  # Для CORS
    'colorfield',  # Для django-colorfield
    'rest_framework.authtoken',  # Добавлено для поддержки токенов в REST API
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Перед CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Разрешаем запросы с фронтенда
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  # Текущий порт фронтенда (Vue по умолчанию)
    "http://localhost:3000",  # Альтернативный порт фронтенда
    "https://boodaikg.com",   # Добавлен домен продакшена
]

# Настройки REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # Поддержка токенов
        'rest_framework.authentication.SessionAuthentication',  # Для админки и браузера
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',  # Чтение для всех, запись для авторизованных
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,  # Количество элементов на странице API (синхронизация с фронтендом)
}

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "shop" / "templates"],  # Путь к шаблонам
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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database configuration based on environment
if DEBUG:
    # SQLite для разработки
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # MySQL для продакшена
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ch79145_boodai',
            'USER': 'ch79145_boodai',
            'PASSWORD': '16162007',
            'HOST': 'vh438.timeweb.ru',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'  # Изменено на русский для локализации
TIME_ZONE = 'Europe/Moscow'  # Часовой пояс (пример для Москвы)
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Папка для разработки
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # Папка для продакшена (collectstatic)

# Media files (Uploaded Images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Настройки для загрузки файлов
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB максимальный размер файла в памяти
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB максимальный размер данных в запросе

# Email settings (для уведомлений, сброса пароля и т.д.)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Вывод в консоль для разработки
# Для продакшена (раскомментируйте и настройте):
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-specific-password'

# Логирование (для отладки)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'shop': {  # Логи для вашего приложения
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Кастомные настройки для django-admin-interface
ADMIN_INTERFACE_THEME = 'modern'  # Тема для django-admin-interface (опционально)