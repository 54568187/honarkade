from django.shortcuts import render
from .models import SiteSetting


class MaintenanceModeMiddleware:
    """
    میدلور بررسی حالت تعمیرات فروشگاه:
    - در صورت غیرفعال بودن فروشگاه، کاربران عادی با پیام سفارشی مواجه می‌شوند.
    - پنل ادمین (/admin/) همواره برای مدیران در دسترس است.
    - IPهای مجاز تعیین شده در تنظیمات می‌توانند نمای فروشگاه را در زمان تعمیرات مشاهده کنند.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # دسترسی به پنل ادمین و فایل‌های استاتیک و مدیا همواره باز است
        if (
            request.path.startswith("/admin/")
            or request.path.startswith("/static/")
            or request.path.startswith("/media/")
        ):
            return self.get_response(request)

        try:
            settings = SiteSetting.load()
            if settings.is_maintenance_mode:
                # اگر کاربر لاگین کرده و کارمند/مدیر است دسترسی دارد
                if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
                    return self.get_response(request)

                # بررسی IP بازدیدکننده
                client_ip = self.get_client_ip(request)
                allowed_ips = [ip.strip() for ip in settings.maintenance_allowed_ips.split(",") if ip.strip()]

                if client_ip in allowed_ips or "127.0.0.1" in allowed_ips and client_ip in ("127.0.0.1", "::1"):
                    return self.get_response(request)

                # نمایش صفحه شیک حالت تعمیرات
                return render(
                    request,
                    "pages/maintenance.html",
                    {"site_settings": settings, "client_ip": client_ip},
                    status=503
                )
        except Exception:
            # در صورت عدم اجرای میگریشن یا خطای اولیه
            pass

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip
