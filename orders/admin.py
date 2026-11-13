from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from core.admin_helpers import render_action_buttons
from .models import Order, OrderItem, CartRule, SettlementRequest


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "unit_price", "total_item_price", "selected_attributes")


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        "id",
        "customer",
        "total_price_display",
        "payment_method_display",
        "status",
        "delivery_schedule_display",
        "carrier",
        "is_gift_display",
        "created_at",
        "action_buttons"
    )
    list_filter = ("status", "payment_method", "is_gift_wrapped", "is_recycled_packaging", "created_at", "carrier")
    list_editable = ("status",)
    search_fields = ("id", "customer__username", "customer__first_name", "customer__last_name", "phone", "address", "bank_tracking_code", "gateway_ref_code")
    readonly_fields = ("total_products_price", "shipping_cost", "total_price", "commission_amount", "paid_at", "created_at", "updated_at")
    inlines = [OrderItemInline]

    fieldsets = (
        ("مشخصات خریدار و وضعیت سفارش", {
            "fields": ("customer", "status", "created_at", "updated_at")
        }),
        ("روش پرداخت و درگاه بانکی / فیش (کارگاه ۱۷)", {
            "fields": (
                "payment_method",
                "gateway_ref_code",
                "card_masked_number",
                "paid_at",
                "bank_tracking_code",
                "bank_receipt_image",
            ),
            "description": "پیکربندی و مشاهده جزئیات پرداخت اینترنتی شاپرک یا فیش بانکی (کارت به کارت)"
        }),
        ("زمان‌بندی ارسال و بازه دریافت کالا", {
            "fields": ("delivery_date", "delivery_time_slot"),
            "description": "روز و بازه زمانی انتخابی خریدار جهت ارسال و دریافت بسته سفارشی."
        }),
        ("خدمات بسته‌بندی ویژه (کتاب درسی)", {
            "fields": ("is_gift_wrapped", "gift_message", "is_recycled_packaging"),
            "description": "کادوپیچی محصول و استفاده از بسته‌بندی قابل بازیافت دوستدار محیط زیست"
        }),
        ("اطلاعات ارسال و حامل انتخابی", {
            "fields": ("carrier", "province", "city", "address", "postal_code", "phone", "notes")
        }),
        ("محاسبه مالی و سهم درآمد پلتفرم", {
            "fields": ("total_products_price", "shipping_cost", "total_price", "commission_rate", "commission_amount"),
            "description": "محاسبه خودکار کارمزد و درآمد پلتفرم از سفارش بر اساس درصد تعریف‌شده."
        }),
    )

    @display(description="روش پرداخت")
    def payment_method_display(self, obj):
        return obj.get_payment_method_display()

    @display(description="زمان تحویل کالا")
    def delivery_schedule_display(self, obj):
        return f"{obj.delivery_date} ({obj.delivery_time_slot})"

    @display(description="کادوپیچی", boolean=True)
    def is_gift_display(self, obj):
        return obj.is_gift_wrapped

    @display(description="عملیات")
    def action_buttons(self, obj):
        return render_action_buttons(obj, edit_label="بررسی", delete_label="حذف")

    def total_price_display(self, obj):
        return f"{obj.total_price:,} تومان"
    total_price_display.short_description = "مبلغ کل"

    def commission_display(self, obj):
        return f"{obj.commission_amount:,} تومان ({obj.commission_rate}٪)"
    commission_display.short_description = "سهم کارمزد هنرکده"


@admin.register(CartRule)
class CartRuleAdmin(ModelAdmin):
    list_display = (
        "id",
        "name",
        "code_display",
        "discount_display",
        "priority",
        "usage_display",
        "valid_to",
        "is_active_badge",
        "action_buttons"
    )
    list_filter = ("is_active", "discount_type", "created_at")
    list_editable = ("priority",)
    search_fields = ("name", "code", "description")

    fieldsets = (
        ("اطلاعات عمومی قانون سبد خرید", {
            "fields": ("name", "description", "code", "priority", "is_active")
        }),
        ("شرایط و مقدار تخفیف", {
            "fields": ("discount_type", "discount_value", "min_purchase", "max_discount_amount")
        }),
        ("محدودیت‌های زمانی و تعداد استفاده", {
            "fields": ("valid_from", "valid_to", "usage_limit", "used_count")
        }),
    )

    @display(description="عملیات")
    def action_buttons(self, obj):
        return render_action_buttons(obj)

    @display(description="کد تخفیف", label=True)
    def code_display(self, obj):
        return obj.code

    @display(description="نوع و مقدار تخفیف")
    def discount_display(self, obj):
        if obj.discount_type == "percentage":
            return f"{obj.discount_value}٪ درصد تخفیف"
        elif obj.discount_type == "fixed":
            return f"{obj.discount_value:,} تومان تخفیف نقدی"
        return "ارسال رایگان"

    @display(description="تعداد استفاده")
    def usage_display(self, obj):
        return f"{obj.used_count} از {obj.usage_limit}"

    @display(description="وضعیت", boolean=True)
    def is_active_badge(self, obj):
        return obj.is_active


@admin.register(SettlementRequest)
class SettlementRequestAdmin(ModelAdmin):
    list_display = (
        "id",
        "booth",
        "amount_display",
        "shaba_number",
        "card_number",
        "status",
        "tracking_code",
        "created_at",
        "action_buttons",
    )
    list_filter = ("status", "created_at")
    list_editable = ("status",)
    search_fields = ("id", "booth__name", "shaba_number", "card_number", "tracking_code", "admin_note")
    fieldsets = (
        ("مشخصات غرفه متقاضی تسویه", {
            "fields": ("booth", "amount", "status")
        }),
        ("اطلاعات بانکی جهت واریز وجه", {
            "fields": ("shaba_number", "card_number", "tracking_code", "admin_note")
        }),
    )

    @display(description="مبلغ درخواستی")
    def amount_display(self, obj):
        return f"{obj.amount:,} تومان"

    @display(description="عملیات")
    def action_buttons(self, obj):
        return render_action_buttons(obj)

