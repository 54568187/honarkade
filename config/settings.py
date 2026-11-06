"""
Django settings for Honarkadeh project.
A professional, production-grade online art marketplace CMS.
"""

from pathlib import Path
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-honarkadeh-marketplace-kadehonar-key-2026'

DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://*.trycloudflare.com",
    "http://*.trycloudflare.com",
    "https://*.ngrok-free.dev",
    "https://*.ngrok-free.app",
    "https://*.kadehonar.ir",
    "https://kadehonar.ir",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

INSTALLED_APPS = [
    # Unfold admin theme
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    
    # Core marketplace applications
    "core.apps.CoreConfig",
    "accounts.apps.AccountsConfig",
    "shipping.apps.ShippingConfig",
    "catalog.apps.CatalogConfig",
    "orders.apps.OrdersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
    # مدیریت وضعیت تعمیرات و دسترسی اضطراری
    "core.middleware.MaintenanceModeMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # تزریق خودکار تنظیمات زنده، دسته‌بندی‌ها، بنرها و منوها به کلیه صفحات
                "core.context_processors.site_context",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "accounts.backends.SmartAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
]

LANGUAGE_CODE = "fa-ir"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# تنظیمات پیشرفته و حرفه‌ای پنل مدیریت Unfold
UNFOLD = {
    "SITE_TITLE": "پنل مدیریت بازارچه هنرکده",
    "SITE_HEADER": "سامانه مدیریت جامع هنرکده (kadehonar.ir)",
    "SITE_URL": "/",
    "SITE_SYMBOL": "palette",
    "STYLES": [
        lambda request: "/static/css/admin_custom.css?v=2.6",
    ],
    "SCRIPTS": [
        lambda request: "/static/js/admin_custom.js",
    ],
    "COLORS": {
        "primary": {
            "50": "#e6f9fc",
            "100": "#ccf2f7",
            "200": "#99e5f0",
            "300": "#5cd4e5",
            "400": "#26bed6",
            "500": "#00a4be",  # فیروزه‌ای اختصاصی پرستاشاپ
            "600": "#008a9f",
            "700": "#007082",
            "800": "#045b6a",
            "900": "#084c58",
            "950": "#02323c",
        },
    },
    "COMMAND": {
        "search_models": True,
        "show_history": True,
    },
    "SIDEBAR": {
        "show_search": True,
        "command_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "هویت و تنظیمات",
                "separator": True,
                "items": [
                    {
                        "title": "تنظیمات و هویت سایت",
                        "icon": "settings",
                        "link": reverse_lazy("admin:core_sitesetting_changelist"),
                    },
                ],
            },
            {
                "title": "کاتالوگ و آثار",
                "separator": True,
                "items": [
                    {
                        "title": "محصولات و آثار هنری",
                        "icon": "palette",
                        "link": reverse_lazy("admin:catalog_product_changelist"),
                    },
                    {
                        "title": "دسته‌بندی‌های آثار",
                        "icon": "category",
                        "link": reverse_lazy("admin:catalog_category_changelist"),
                    },
                    {
                        "title": "مشخصه‌های متغیر",
                        "icon": "tune",
                        "link": reverse_lazy("admin:catalog_attribute_changelist"),
                    },
                    {
                        "title": "ویژگی‌های فنی کالا",
                        "icon": "featured_play_list",
                        "link": reverse_lazy("admin:catalog_feature_changelist"),
                    },
                    {
                        "title": "برندها و نشان‌ها",
                        "icon": "verified",
                        "link": reverse_lazy("admin:catalog_brand_changelist"),
                    },
                    {
                        "title": "تأمین‌کنندگان کالا",
                        "icon": "inventory",
                        "link": reverse_lazy("admin:catalog_supplier_changelist"),
                    },
                ],
            },
            {
                "title": "بازارچه و هنرمندان",
                "separator": True,
                "items": [
                    {
                        "title": "غرفه‌های هنرمندان",
                        "icon": "storefront",
                        "link": reverse_lazy("admin:catalog_booth_changelist"),
                    },
                ],
            },
            {
                "title": "طراحی و بازاریابی",
                "separator": True,
                "items": [
                    {
                        "title": "اسلایدر صفحه اول",
                        "icon": "view_carousel",
                        "link": reverse_lazy("admin:core_slider_changelist"),
                    },
                    {
                        "title": "بنرهای تبلیغاتی",
                        "icon": "ad_units",
                        "link": reverse_lazy("admin:core_banner_changelist"),
                    },
                    {
                        "title": "منوی ناوبری سایت",
                        "icon": "menu",
                        "link": reverse_lazy("admin:core_menuitem_changelist"),
                    },
                    {
                        "title": "صفحات ایستا و راهنما",
                        "icon": "article",
                        "link": reverse_lazy("admin:core_staticpage_changelist"),
                    },
                ],
            },
            {
                "title": "ارسال و لجستیک",
                "separator": True,
                "items": [
                    {
                        "title": "روش‌های ارسال کالا",
                        "icon": "local_shipping",
                        "link": reverse_lazy("admin:shipping_carrier_changelist"),
                    },
                    {
                        "title": "استان‌های تحت پوشش",
                        "icon": "map",
                        "link": reverse_lazy("admin:shipping_province_changelist"),
                    },
                    {
                        "title": "مناطق توزیع مرسوله",
                        "icon": "public",
                        "link": reverse_lazy("admin:shipping_region_changelist"),
                    },
                ],
            },
            {
                "title": "فروش و مالی",
                "separator": True,
                "items": [
                    {
                        "title": "سفارش‌ها و کارمزد",
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:orders_order_changelist"),
                    },
                    {
                        "title": "کدهای تخفیف و پروموشن",
                        "icon": "confirmation_number",
                        "link": reverse_lazy("admin:orders_cartrule_changelist"),
                    },
                ],
            },
            {
                "title": "مدیریت مشتریان",
                "separator": True,
                "items": [
                    {
                        "title": "مشتریان و خریداران هنر",
                        "icon": "groups",
                        "link": reverse_lazy("admin:accounts_customer_changelist"),
                    },
                ],
            },
            {
                "title": "پرسنل و دسترسی‌ها",
                "separator": True,
                "items": [
                    {
                        "title": "پرسنل و کارمندان سامانه",
                        "icon": "badge",
                        "link": reverse_lazy("admin:accounts_staffuser_changelist"),
                    },
                    {
                        "title": "نقش‌ها و مجوزهای دسترسی",
                        "icon": "admin_panel_settings",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
}
