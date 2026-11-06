from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from catalog.models import Product
from shipping.models import Carrier, Province


class Order(models.Model):
    """سفارش‌های مشتریان و ثبت کارمزد پلتفرم"""
    STATUS_CHOICES = (
        ("pending", _("در انتظار پرداخت")),
        ("processing", _("در حال آماده‌سازی توسط هنرمند")),
        ("shipped", _("تحویل به شرکت حمل‌ونقل و ارسال")),
        ("delivered", _("تحویل مرسوله به مشتری")),
        ("canceled", _("لغو شده")),
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("مشتری / خریدار")
    )
    carrier = models.ForeignKey(
        Carrier,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders",
        verbose_name=_("حامل انتخابی (روش ارسال)")
    )
    
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("استان مقصد")
    )
    city = models.CharField(max_length=100, verbose_name=_("شهر مقصد"))
    address = models.TextField(verbose_name=_("آدرس دقیق پستی"))
    postal_code = models.CharField(max_length=20, verbose_name=_("کد پستی ۱۰ رقمی"))
    phone = models.CharField(max_length=20, verbose_name=_("شماره تماس تحویل‌گیرنده"))
    notes = models.TextField(blank=True, verbose_name=_("یادداشت مشتری"))

    total_products_price = models.PositiveIntegerField(
        default=0,
        verbose_name=_("مجموع مبلغ محصولات (تومان)")
    )
    shipping_cost = models.PositiveIntegerField(
        default=0,
        verbose_name=_("هزینه ارسال (تومان)")
    )
    total_price = models.PositiveIntegerField(
        default=0,
        verbose_name=_("مبلغ کل سفارش (تومان)")
    )
    commission_rate = models.PositiveIntegerField(
        default=10,
        verbose_name=_("درصد کارمزد پلتفرم (%)"),
        help_text=_("درصد سهم هنرکده از این سفارش (مثلاً ۱۰٪)")
    )
    commission_amount = models.PositiveIntegerField(
        default=0,
        verbose_name=_("سهم درآمد پلتفرم (تومان)")
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("وضعیت سفارش")
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("زمان ثبت سفارش"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخرین تغییر وضعیت"))

    class Meta:
        verbose_name = _("سفارش")
        verbose_name_plural = _("سفارش‌های مشتریان")
        ordering = ["-created_at"]

    def __str__(self):
        return f"سفارش شماره #{self.id} - خریدار: {self.customer.get_full_name() or self.customer.username} ({self.total_price:,} تومان)"

    def save(self, *args, **kwargs):
        self.total_price = self.total_products_price + self.shipping_cost
        if self.total_products_price > 0 and self.commission_rate > 0:
            self.commission_amount = int((self.total_products_price * self.commission_rate) / 100)
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """اقلام موجود در هر سفارش"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("سفارش مربوطه")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name=_("محصول / اثر")
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("تعداد"))
    unit_price = models.PositiveIntegerField(verbose_name=_("قیمت واحد در زمان خرید (تومان)"))
    selected_attributes = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("مشخصات انتخابی (سایز، رنگ، طرح)")
    )

    class Meta:
        verbose_name = _("قلم سفارش")
        verbose_name_plural = _("اقلام سفارش‌ها")

    def __str__(self):
        return f"{self.quantity} عدد {self.product.name} در سفارش #{self.order.id}"

    @property
    def total_item_price(self):
        if self.quantity is not None and self.unit_price is not None:
            return self.quantity * self.unit_price
        return 0


class CartRule(models.Model):
    """
    قوانین سبد خرید و کدهای تخفیف (مشابه سیستم پرستاشاپ)
    امکان تعریف کدهای تخفیف درصدی، مبلغ ثابت، حداقل خرید و تاریخ انقضا
    """
    DISCOUNT_TYPES = (
        ("percentage", _("درصد تخفیف (%)")),
        ("fixed", _("مبلغ ثابت (تومان)")),
        ("free_shipping", _("ارسال رایگان مرسوله")),
    )

    name = models.CharField(max_length=200, verbose_name=_("نام قانون سبد خرید"))
    description = models.TextField(blank=True, verbose_name=_("توضیحات و شرایط استفاده"))
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("کد تخفیف (جهت درج توسط خریدار)")
    )
    priority = models.PositiveIntegerField(
        default=1,
        verbose_name=_("اولویت اعمال"),
        help_text=_("در صورت وجود چند قانون، اولویت کمتر زودتر اعمال می‌شود.")
    )
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPES,
        default="percentage",
        verbose_name=_("نوع تخفیف")
    )
    discount_value = models.PositiveIntegerField(
        default=15,
        verbose_name=_("مقدار تخفیف (درصد یا تومان)"),
        help_text=_("برای درصدی مثلاً ۱۵ و برای مبلغ ثابت مثلاً ۵۰۰۰۰")
    )
    min_purchase = models.PositiveIntegerField(
        default=0,
        verbose_name=_("حداقل مبلغ خرید برای اعمال (تومان)")
    )
    max_discount_amount = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name=_("سقف مبلغ تخفیف (تومان - ۰ برای نامحدود)")
    )
    usage_limit = models.PositiveIntegerField(
        default=100,
        verbose_name=_("سقف کل تعداد استفاده")
    )
    used_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("تعداد دفعات استفاده شده")
    )
    valid_from = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("معتبر از تاریخ و ساعت")
    )
    valid_to = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("تاریخ انقضاء")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("وضعیت فعال بودن")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ثبت"))

    class Meta:
        verbose_name = _("قانون سبد خرید (کد تخفیف)")
        verbose_name_plural = _("قوانین سبد خرید و تخفیف‌ها")
        ordering = ["priority", "-created_at"]

    def __str__(self):
        return f"{self.name} ({self.code})"

