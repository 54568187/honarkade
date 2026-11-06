from .models import SiteSetting, Banner, MenuItem, StaticPage
from catalog.models import Category


def site_context(request):
    """
    توزیع خودکار داده‌های زنده و پویای فروشگاه به تمام صفحات و کامپوننت‌های فرانت‌اند
    """
    try:
        settings = SiteSetting.load()
    except Exception:
        settings = None

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
    }
