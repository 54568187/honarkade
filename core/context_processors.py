from .models import SiteSetting, Banner, MenuItem, StaticPage, ThemeTranslation
from catalog.models import Category


def site_context(request):
    """
    توزیع خودکار داده‌های زنده و پویای فروشگاه به تمام صفحات و کامپوننت‌های فرانت‌اند
    همراه با پشتیبانی کامل از ترجمه قالب و دو زبانه بودن (فارسی / انگلیسی)
    """
    try:
        settings = SiteSetting.load()
    except Exception:
        settings = None

    # تعیین زبان فعال تارنما: ابتدا پارامتر GET، سپس کوکی، در غیر این صورت فارسی
    lang = request.GET.get("lang") or request.COOKIES.get("site_lang") or "fa"
    lang = "en" if lang.lower() in ("en", "english") else "fa"
    is_en = (lang == "en")
    site_dir = "ltr" if is_en else "rtl"

    # بارگذاری عبارات ترجمه قالب (کارگاه ۱۹ کتاب درسی)
    trans_map = {}
    try:
        for item in ThemeTranslation.objects.all():
            trans_map[item.key] = item.en_translation if is_en else item.fa_translation
    except Exception:
        pass

    top_banner = Banner.objects.filter(position="top", is_active=True).first()
    menu_items = MenuItem.objects.filter(is_active=True, parent__isnull=True).prefetch_related("children")
    footer_pages = StaticPage.objects.filter(is_active=True, show_in_footer=True)
    header_categories = Category.objects.filter(is_active=True, parent__isnull=True).prefetch_related("children")

    return {
        "site_settings": settings,
        "top_banner": top_banner,
        "main_menu_items": menu_items,
        "footer_pages": footer_pages,
        "header_categories": header_categories,
        "current_lang": lang,
        "is_en": is_en,
        "site_dir": site_dir,
        "t": trans_map,
    }
