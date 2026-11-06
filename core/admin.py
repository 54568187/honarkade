from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from core.admin_helpers import render_action_buttons
from .models import SiteSetting, StaticPage, Slider, Banner, MenuItem


@admin.register(SiteSetting)
class SiteSettingAdmin(ModelAdmin):
    list_display = ("title", "email", "phone", "currency", "is_maintenance_mode")
    fieldsets = (
        ("اطلاعات عمومی و تماس فروشگاه", {
            "fields": ("title", "tagline", "email", "phone", "address", "currency"),
            "description": "پیکربندی هویت پایه فروشگاه که به بازدیدکنندگان و در فاکتورها نمایش داده می‌شود."
        }),
        ("لوگو و نشان‌های تصویری", {
            "fields": ("header_logo", "invoice_logo", "favicon"),
            "description": "نشان تصویری سربرگ سایت، لوگوی فاکتور و آیکون مرورگر (Favicon)."
        }),
        ("وضعیت نگهداری و تعمیرات", {
            "fields": ("is_maintenance_mode", "maintenance_allowed_ips", "maintenance_message"),
            "description": "تعلیق موقت فروشگاه برای بازدیدکنندگان عادی و تعیین آدرس‌های IP مجاز."
        }),
        ("تنظیمات اسلایدر و کپی‌رایت فوتر", {
            "fields": ("slider_speed", "slider_stop_at_end", "footer_copyright"),
        }),
        ("محتوای بخش‌های صفحه اصلی و ویترین آثار", {
            "fields": ("hero_showcase_title", "hero_showcase_subtitle"),
            "description": "تغییر عنوان و زیرعنوان ویترین دست‌سازه‌ها در صفحه نخست."
        }),
        ("بنر فراخوان و جذب هنرمندان (صفحه اصلی)", {
            "fields": ("call_to_action_badge", "call_to_action_title", "call_to_action_desc", "call_to_action_btn", "call_to_action_url"),
            "description": "متون و دکمه بنر انتهای صفحه اصلی جهت دعوت و ثبت‌نام هنرمندان."
        }),
        ("مزایای خرید و اعتماد در فوتر سایت", {
            "fields": (
                ("benefit_1_title", "benefit_1_desc"),
                ("benefit_2_title", "benefit_2_desc"),
                ("benefit_3_title", "benefit_3_desc"),
                ("benefit_4_title", "benefit_4_desc"),
            ),
            "description": "ویرایش ۴ نشان اعتماد فوتر (شناسنامه، بسته‌بندی، ضمانت بازگشت و مشاوره)."
        }),
    )

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(StaticPage)
class StaticPageAdmin(ModelAdmin):
    list_display = ("title", "slug", "show_in_footer", "is_active", "order", "action_buttons")
    list_editable = ("show_in_footer", "is_active", "order")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("مشخصات صفحه", {
            "fields": ("title", "slug", "content", "show_in_footer", "is_active", "order")
        }),
        ("بهینه‌سازی موتورهای جستجو (سئو)", {
            "fields": ("meta_title", "meta_description"),
            "classes": ("collapse",),
        }),
    )

    @display(description="عملیات")
    def action_buttons(self, obj):
        return render_action_buttons(obj)


@admin.register(Slider)
class SliderAdmin(ModelAdmin):
    list_display = ("image_preview", "title", "order", "is_active", "link", "action_buttons")
    list_editable = ("order", "is_active")
    search_fields = ("title", "subtitle")
    fieldsets = (
        ("پیکربندی اسلاید", {
            "fields": ("title", "subtitle", "image", "link", "button_text", "order", "is_active")
        }),
    )

    @display(description="پیش‌نمایش تصویر")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" class="admin-thumbnail" style="width: 70px; height: 35px; border-radius: 6px;" alt="{}" />',
                obj.image.url,
                obj.title
            )
        return format_html('<span class="text-xs text-slate-400">-</span>')

    @display(description="عملیات")
    def action_buttons(self, obj):
        return render_action_buttons(obj)


@admin.register(Banner)
class BannerAdmin(ModelAdmin):
    list_display = ("image_preview", "title", "position", "discount_code", "is_active", "action_buttons")
    list_editable = ("is_active",)
    list_filter = ("position", "is_active")
    fieldsets = (
        ("پیکربندی بنر", {
            "fields": ("title", "description", "discount_code", "image", "alt_text", "link", "position", "is_active")
        }),
    )

    @display(description="پیش‌نمایش تصویر")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" class="admin-thumbnail" style="width: 70px; height: 35px; border-radius: 6px;" alt="{}" />',
                obj.image.url,
                obj.title
            )
        return format_html('<span class="text-xs text-slate-400">-</span>')

    @display(description="عملیات")
    def action_buttons(self, obj):
        return render_action_buttons(obj)


@admin.register(MenuItem)
class MenuItemAdmin(ModelAdmin):
    list_display = ("title", "url", "parent", "order", "is_active", "action_buttons")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "url")

    @display(description="عملیات")
    def action_buttons(self, obj):
        return render_action_buttons(obj)
