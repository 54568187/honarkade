from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from catalog.models import Product, Booth
from shipping.models import Carrier, Province


class Order(models.Model):
    """سفارش‌های مشتریان و ثبت کارمزد پلتفرم"""
    STATUS_CHOICES = (
        ("pending", _("در انتظار پرداخت")),
        ("remote_paid", _("پرداخت از راه دور تأیید شده (فیش بانکی)")),
        ("processing", _("در حال آماده‌سازی توسط هنرمند")),
        ("shipped", _("تحویل به شرکت حمل‌ونقل و ارسال")),
        ("delivered", _("تحویل مرسوله به مشتری")),
        ("canceled", _("لغو شده")),
    )

    PAYMENT_METHOD_CHOICES = (
        ("online", _("درگاه پرداخت اینترنتی")),
        ("bank_transfer", _("پرداخت از طریق فیش بانکی (کارت به کارت)")),
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

    # روش پرداخت و فیش بانکی (کارگاه ۱۷ کتاب درسی)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="online",
        verbose_name=_("روش پرداخت")
    )
    bank_tracking_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("شماره پیگیری فیش بانکی")
    )
    bank_receipt_image = models.ImageField(
        upload_to="receipts/",
        blank=True,
        null=True,
        verbose_name=_("تصویر فیش واریزی")
    )

    # بسته‌بندی هدیه و بسته‌بندی بازیافتی (مبحث بسته‌بندی کتاب درسی)
    is_gift_wrapped = models.BooleanField(
        default=False,
        verbose_name=_("کادوپیچی محصول (بسته‌بندی هدیه)")
    )
    gift_message = models.TextField(
        blank=True,
        verbose_name=_("پیام تبریک روی کارت هدیه")
    )
    is_recycled_packaging = models.BooleanField(
        default=False,
        verbose_name=_("بسته‌بندی بازیافتی (دوستدار محیط زیست)")
    )

    # بازه زمانی دریافت و روز ارسال کالا
    delivery_date = models.CharField(
        max_length=100,
        blank=True,
        default="سریع‌ترین زمان ممکن (۱ الی ۳ روز کاری)",
        verbose_name=_("روز انتخابی دریافت کالا")
    )
    delivery_time_slot = models.CharField(
        max_length=100,
        blank=True,
        default="ساعت ۹ الی ۱۳ (صبح)",
        verbose_name=_("بازه ساعتی تحویل مرسوله")
    )

    # اطلاعات تراکنش شاپرک و درگاه بانکی
    gateway_ref_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("کد پیگیری شاپرک / مرجع تراکنش آنلاین")
    )
    card_masked_number = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_("شماره کارت خریدار (ماسک شده)")
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("زمان پرداخت درگاه")
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




class SettlementRequest(models.Model):
    """درخواست‌های تسویه حساب مالی غرفه‌داران"""
    STATUS_CHOICES = (
        ("pending", _("در انتظار بررسی و واریز پایا")),
        ("paid", _("واریز شد و تسویه گردید")),
        ("rejected", _("رد شده")),
    )
    booth = models.ForeignKey(
        Booth,
        on_delete=models.CASCADE,
        related_name="settlement_requests",
        verbose_name=_("غرفه درخواست‌دهنده")
    )
    amount = models.PositiveIntegerField(verbose_name=_("مبلغ درخواستی تسویه (تومان)"))
    shaba_number = models.CharField(max_length=40, verbose_name=_("شماره شبا مقصد"))
    card_number = models.CharField(max_length=30, blank=True, verbose_name=_("شماره کارت مقصد"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name=_("وضعیت درخواست"))
    tracking_code = models.CharField(max_length=100, blank=True, verbose_name=_("کد پیگیری حواله پایا/ساتنا"))
    admin_note = models.TextField(blank=True, verbose_name=_("توضیحات مدیر مالی"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ثبت درخواست"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاریخ به‌روزرسانی"))

    class Meta:
        verbose_name = _("درخواست تسویه حساب غرفه‌دار")
        verbose_name_plural = _("درخواست‌های تسویه حساب غرفه‌داران")
        ordering = ["-created_at"]

    def __str__(self):
        return f"درخواست #{self.id} - غرفه: {self.booth.name} ({self.amount:,} تومان) - {self.get_status_display()}"
