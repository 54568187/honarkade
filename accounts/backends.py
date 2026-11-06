from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from accounts.models import UserProfile

PERSIAN_ARABIC_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')


def normalize_input(text):
    if not text:
        return text
    return text.translate(PERSIAN_ARABIC_DIGITS).strip()


class SmartAuthenticationBackend(ModelBackend):
    """
    سیستم احراز هویت هوشمند برای هنرکده:
    ۱. تبدیل خودکار اعداد فارسی/عربی کیبورد (۱۲۳۴ -> 1234) در نام کاربری و رمز عبور
    ۲. پشتیبانی از ورود با نام کاربری، ایمیل یا شماره موبایل
    ۳. عدم حساسیت نام کاربری به بزرگی و کوچکی حروف (Case-insensitive)
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        # نرمال‌سازی ارقام فارسی/عربی
        raw_username = username.strip()
        clean_username = normalize_input(raw_username)

        # جستجوی کاربر از طریق نام کاربری، ایمیل یا شماره همراه در پروفایل
        user = None
        user = User.objects.filter(
            Q(username__iexact=raw_username) |
            Q(username__iexact=clean_username) |
            Q(email__iexact=raw_username) |
            Q(email__iexact=clean_username)
        ).first()

        if not user:
            # جستجو در شماره تماس پروفایل
            profile = UserProfile.objects.filter(
                Q(phone_number=raw_username) | Q(phone_number=clean_username)
            ).first()
            if profile:
                user = profile.user

        if user:
            # تست پسورد اصلی
            if user.check_password(password):
                return user
            # تست پسورد پس از تبدیل ارقام فارسی به انگلیسی (برای کاربرانی که با کیبورد فارسی پسورد زدند)
            clean_password = normalize_input(password)
            if clean_password != password and user.check_password(clean_password):
                return user

        return None
