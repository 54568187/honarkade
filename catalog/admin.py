from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from core.admin_helpers import render_action_buttons
from .models import (
    Category, Attribute, AttributeValue, Feature, FeatureValue,
    Brand, Supplier, Booth, Product, ProductImage
)


class AttributeValueInline(TabularInline):
    model = AttributeValue
    extra = 2
    fields = ("value", "color_code")


@admin.register(Attribute)
class AttributeAdmin(ModelAdmin):
    list_display = ("public_name", "name", "attribute_type", "action_buttons")
    search_fields = ("public_name", "name")
    inlines = [AttributeValueInline]

    @display(description="عملیات")
    def action_buttons(self, obj):
        return render_action_buttons(obj)


class FeatureValueInline(TabularInline):
    model = FeatureValue
    extra = 2
    fields = ("value",)


@admin.register(Feature)
class FeatureAdmin(ModelAdmin):
    list_display = ("name", "action_buttons")
    search_fields = ("name",)
    inlines = [FeatureValueInline]

    @display(description="عملیات")
    def action_buttons(self, obj):
        return render_action_buttons(obj)


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("image_preview", "name", "parent", "is_active", "order", "action_buttons")
    list_editable = ("is_active", "order")
    list_filter = ("is_active", "parent")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("مشخصات شاخه", {
            "fields": ("name", "slug", "parent", "is_active", "description", "order")
        }),
        ("تصاویر شاخه", {
            "fields": ("image", "thumbnail"),
        }),
        ("بهینه‌سازی موتورهای جستجو (سئو)", {
            "fields": ("meta_title", "meta_description"),
            "classes": ("collapse",),
        }),
    )

    @display(description="تصویر شاخه")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" class="admin-thumbnail" alt="{}" />',
                obj.image.url,
                obj.name
            )
        return format_html('<span class="text-xs text-slate-400">-</span>')

    @display(description="عملیات")
    def action_buttons(self, obj):
        return render_action_buttons(obj)


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ("logo_preview", "name", "admin_phone", "is_active", "action_buttons")
    search_fields = ("name", "admin_phone", "admin_address")
    fieldsets = (
        ("مشخصات عمومی برند", {
            "fields": ("name", "logo", "description", "is_active")
        }),
        ("دفترچه تلفن و نشانی محرمانه مدیران", {
            "fields": ("admin_phone", "admin_address"),
            "description": "نشانی و تلفن‌هایی که برای بازدیدکنندگان سایت نمایش داده نمی‌شود و فقط در پنل مدیریت قابل مشاهده است."
        }),
    )

    @display(description="لوگو")
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" class="admin-thumbnail" alt="{}" />',
                obj.logo.url,
                obj.name
            )
        return format_html('<span class="text-xs text-slate-400">-</span>')

    @display(description="عملیات")
    def action_buttons(self, obj):
        return render_action_buttons(obj)


@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = ("name", "contact_person", "phone", "action_buttons")
    search_fields = ("name", "contact_person", "phone")

    @display(description="عملیات")
    def action_buttons(self, obj):
        return render_action_buttons(obj)


@admin.register(Booth)
class BoothAdmin(ModelAdmin):
    list_display = ("name", "owner", "is_approved", "created_at", "action_buttons")
    list_filter = ("is_approved",)
    list_editable = ("is_approved",)
    search_fields = ("name", "owner__username", "owner__first_name", "owner__last_name")
    prepopulated_fields = {"slug": ("name",)}
    actions = ["approve_booths", "reject_booths"]

    @display(description="عملیات")
    def action_buttons(self, obj):
        return render_action_buttons(obj)

    @admin.action(description="تأیید غرفه‌های انتخاب شده")
    def approve_booths(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="عدم تأیید / تعلیق غرفه‌های انتخاب شده")
    def reject_booths(self, request, queryset):
        queryset.update(is_approved=False)


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "alt_text")


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = (
        "image_preview",
        "name",
        "booth",
        "category",
        "brand",
        "weight_display",
        "price_display",
        "stock",
        "has_physical_certificate_badge",
        "is_approved",
        "status",
        "is_featured",
        "action_buttons"
    )
    list_editable = ("stock", "is_approved", "status", "is_featured")
    list_filter = ("has_physical_certificate", "is_approved", "status", "is_featured", "category", "brand")
    search_fields = ("name", "sku", "description", "booth__name")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("attributes", "features")
    inlines = [ProductImageInline]
    actions = ["approve_products", "unapprove_products"]

    fieldsets = (
        ("اطلاعات عمومی اثر هنری", {
            "fields": ("name", "slug", "booth", "image")
        }),
        ("شناسنامه فنی اثر (دسته‌بندی، نشان تجاری، وزن، سایز، بافت و گواهی اصالت)", {
            "fields": (
                "category",
                "brand",
                "weight",
                "attributes",
                "features",
                "has_physical_certificate",
                "certificate_description",
            ),
            "description": "مدیریت کلیه آیتم‌های شناسنامه فنی اثر: شاخه دسته‌بندی، نشان تجاری، وزن کالا (گرم)، مشخصه‌های متغیر (اندازه و سایز اثر، رنگ‌بندی)، ویژگی‌های فنی (بافت، جنس) و وضعیت گواهی شناسنامه فیزیکی."
        }),
        ("قیمت‌گذاری و انبارداری", {
            "fields": ("price", "discount_price", "stock", "sku", "supplier")
        }),
        ("توضیحات و داستان اثر", {
            "fields": ("short_description", "description", "tags")
        }),
        ("وضعیت انتشار و تأیید مدیریت", {
            "fields": ("is_approved", "status", "is_featured")
        }),
    )

    @display(description="عملیات")
    def action_buttons(self, obj):
        return render_action_buttons(obj)

    @display(description="تصویر اثر")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" class="admin-thumbnail" alt="{}" />',
                obj.image.url,
                obj.name
            )
        return format_html('<span class="text-xs text-slate-400">بدون تصویر</span>')

    def price_display(self, obj):
        if obj.discount_price:
            return f"{obj.discount_price:,} تومان (تخفیف‌دار از {obj.price:,})"
        return f"{obj.price:,} تومان"
    price_display.short_description = "قیمت نهایی"

    def weight_display(self, obj):
        return f"{obj.weight:,} گرم"
    weight_display.short_description = "وزن اثر"

    @display(description="شناسنامه فیزیکی", boolean=True)
    def has_physical_certificate_badge(self, obj):
        return obj.has_physical_certificate

    @admin.action(description="تأیید آثار هنری انتخاب شده جهت نمایش در فروشگاه")
    def approve_products(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="عدم تأیید / تعلیق آثار هنری انتخاب شده")
    def unapprove_products(self, request, queryset):
        queryset.update(is_approved=False)

