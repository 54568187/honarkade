"""
WSGI config for Honarkadeh project.
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# تحویل مستقیم فایل‌های استاتیک و تصاویر مدیا از طریق وایت‌نویز
static_root = Path(settings.STATIC_ROOT)
media_root = Path(settings.MEDIA_ROOT)

if static_root.exists():
    application = WhiteNoise(application, root=str(static_root))
else:
    application = WhiteNoise(application)

if media_root.exists():
    application.add_files(str(media_root), prefix=settings.MEDIA_URL)
