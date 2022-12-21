import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kabak_db',
        'USER': 'kabak_user',
        'PASSWORD': 'bkmz18407()',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
FILE_UPLOAD_PERMISSIONS = 0o777

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
