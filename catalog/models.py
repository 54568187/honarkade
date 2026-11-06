from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Category(models.Model):
    """شاخه‌ها و زیرشاخه‌ها"""
    name = models.CharField(
        max_length=150,
        verbose_name=_("نام شاخه (دسته)")
    )
    slug = models.SlugField(
        max_length=180,
        unique=True,
        allow_unicode=True,
        verbose_name=_("URL آشنا (پیوند یکتا)")
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("شاخه والد (در صورت زیرشاخه بودن)")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("نمایش در سایت")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("توضیحات شاخه")
    )
    image = models.ImageField(
        upload_to="categories/covers/",
        blank=True,
        null=True,
        verbose_name=_("عکس نمای دسته‌بندی")
    )
    thumbnail = models.ImageField(
        upload_to="categories/thumbs/",
        blank=True,
        null=True,
        verbose_name=_("تصویر کوچک (بندانگشتی)")
    )
    meta_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("عنوان متا (سئو)")
    )
    meta_description = models.TextField(
        blank=True,
        verbose_name=_("توضیحات متا (سئو)")
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("ترتیب نمایش")
    )

    class Meta:
        verbose_name = _("شاخه (دسته‌بندی)")
        verbose_name_plural = _("شاخه‌ها و دسته‌بندی‌ها")
        ordering = ["order", "name"]

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} » {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Attribute(models.Model):
    """تعریف مشخصه‌های متغیر (سایز، رنگ، طرح)"""
    TYPE_CHOICES = (
        ("select", _("فهرست کشویی (Select)")),
        ("radio", _("دکمه‌های انتخابی (Radio)")),
        ("color", _("رنگ یا بافت (Color Picker)")),
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_("نام داخلی (در پنل مدیریت)")
    )
    public_name = models.CharField(
        max_length=100,
        verbose_name=_("نام عمومی (نمایش به مشتری)")
    )
    attribute_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="select",
        verbose_name=_("نوع مشخصه")
    )

    class Meta:
        verbose_name = _("مشخصه")
        verbose_name_plural = _("مشخصه‌های متغیر (سایز، رنگ، طرح)")

    def __str__(self):
        return f"{self.public_name} ({self.get_attribute_type_display()})"


class AttributeValue(models.Model):
    """مقادیر مشخصه"""
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="values",
        verbose_name=_("مشخصه مربوطه")
    )
    value = models.CharField(
        max_length=100,
        verbose_name=_("مقدار مشخصه")
    )
    color_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("کد رنگ (اختیاری - مانند #2C4A3E)")
    )

    class Meta:
        verbose_name = _("مقدار مشخصه")
        verbose_name_plural = _("مقادیر مشخصه‌ها")
        ordering = ["attribute", "id"]

    def __str__(self):
        return f"{self.attribute.public_name}: {self.value}"


class Feature(models.Model):
    """تعریف ویژگی‌های فنی ثابت (جنس، بافت، تکنیک ساخت)"""
    name = models.CharField(
        max_length=150,
        verbose_name=_("نام ویژگی فنی")
    )

    class Meta:
        verbose_name = _("ویژگی فنی")
        verbose_name_plural = _("ویژگی‌های فنی محصول")

    def __str__(self):
        return self.name


class FeatureValue(models.Model):
    """مقادیر ویژگی"""
    feature = models.ForeignKey(
        Feature,
        on_delete=models.CASCADE,
        related_name="values",
        verbose_name=_("ویژگی مربوطه")
    )
    value = models.CharField(
        max_length=150,
        verbose_name=_("مقدار ویژگی")
    )

    class Meta:
        verbose_name = _("مقدار ویژگی")
        verbose_name_plural = _("مقادیر ویژگی‌ها")

    def __str__(self):
        return f"{self.feature.name}: {self.value}"


class Brand(models.Model):
    """برندها و نشان‌های تجاری"""
    name = models.CharField(
        max_length=150,
        verbose_name=_("نام برند (نشانه تجاری)")
    )
    logo = models.ImageField(
        upload_to="brands/logos/",
        blank=True,
        null=True,
        verbose_name=_("تصویر آرم یا نشان تجاری (لوگو)")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("معرفی کوتاه برند")
    )
    admin_address = models.TextField(
        blank=True,
        verbose_name=_("نشانی برند (دفترچه تلفن مدیران)")
    )
    admin_phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("تلفن تماس برند (دفترچه تلفن مدیران)")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("فعال بودن برند")
    )

    class Meta:
        verbose_name = _("برند (نشان تجاری)")
        verbose_name_plural = _("برندها و نشان‌های تجاری")

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """تأمین‌کنندگان کالا"""
    name = models.CharField(
        max_length=150,
        verbose_name=_("نام تأمین‌کننده")
    )
    contact_person = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("نام شخص رابط")
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("شماره تماس")
    )
    address = models.TextField(
        blank=True,
        verbose_name=_("نشانی تأمین‌کننده")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("توضیحات و شرایط همکاری")
    )

    class Meta:
        verbose_name = _("تأمین‌کننده")
        verbose_name_plural = _("تأمین‌کنندگان کالا")

    def __str__(self):
        return self.name


class Booth(models.Model):
    """غرفه اختصاصی هنرمند در بازارچه آنلاین هنرکده"""
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="booth",
        verbose_name=_("هنرمند و صاحب غرفه")
    )
    name = models.CharField(
        max_length=150,
        verbose_name=_("نام غرفه هنری")
    )
    slug = models.SlugField(
        max_length=180,
        unique=True,
        allow_unicode=True,
        verbose_name=_("URL آشنا غرفه")
    )
    logo = models.ImageField(
        upload_to="booths/logos/",
        blank=True,
        null=True,
        verbose_name=_("نشان و تصویر غرفه")
    )
    banner = models.ImageField(
        upload_to="booths/banners/",
        blank=True,
        null=True,
        verbose_name=_("بنر سربرگ غرفه")
    )
    bio = models.TextField(
        blank=True,
        verbose_name=_("معرفی کوتاه هنرمند و داستان دست‌سازه‌ها")
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name=_("تأیید شده توسط مدیریت بازارچه"),
        help_text=_("پس از بررسی، تیک تأیید را بزنید تا غرفه فعال شود.")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ثبت غرفه"))

    class Meta:
        verbose_name = _("غرفه هنرمند")
        verbose_name_plural = _("غرفه‌های اختصاصی هنرمندان")
        ordering = ["-created_at"]

    def __str__(self):
        status = " (تأیید شده)" if self.is_approved else " (در انتظار تأیید)"
        return f"{self.name} - هنرمند: {self.owner.get_full_name() or self.owner.username}{status}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Product(models.Model):
    """محصول و اثر هنری"""
    STATUS_CHOICES = (
        ("published", _("منتشر شده")),
        ("draft", _("پیش‌نویس")),
    )

    name = models.CharField(max_length=255, verbose_name=_("نام اثر هنری / محصول"))
    slug = models.SlugField(
        max_length=255,
        unique=True,
        allow_unicode=True,
        verbose_name=_("URL آشنا (پیوند یکتا)")
    )
    booth = models.ForeignKey(
        Booth,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("غرفه و هنرمند تولیدکننده")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("شاخه (دسته‌بندی)")
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name=_("برند یا نشان تجاری")
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name=_("تأمین‌کننده")
    )

    image = models.ImageField(
        upload_to="products/main/",
        verbose_name=_("تصویر اصلی اثر")
    )
    price = models.PositiveIntegerField(verbose_name=_("قیمت اصلی (تومان)"))
    discount_price = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("قیمت با تخفیف ویژه (تومان)")
    )
    stock = models.PositiveIntegerField(default=1, verbose_name=_("موجودی در انبار"))
    weight = models.PositiveIntegerField(
        default=500,
        verbose_name=_("وزن کالا به گرم (جهت محاسبه هزینه پست)")
    )
    sku = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("شناسه کالا (SKU / کد محصول)")
    )

    short_description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name=_("توضیحات کوتاه اثر")
    )
    description = models.TextField(verbose_name=_("توضیحات کامل و داستان خلق اثر"))

    attributes = models.ManyToManyField(
        AttributeValue,
        blank=True,
        related_name="products",
        verbose_name=_("مشخصه‌های متغیر (سایز، رنگ، طرح)")
    )
    features = models.ManyToManyField(
        FeatureValue,
        blank=True,
        related_name="products",
        verbose_name=_("ویژگی‌های فنی ثابت (جنس، بافت)")
    )

    has_physical_certificate = models.BooleanField(
        default=True,
        verbose_name=_("دارای شناسنامه فیزیکی معتبر"),
        help_text=_("آیا اثر همراه با گواهی شناسنامه فیزیکی و هولوگرام ارسال می‌شود؟")
    )
    certificate_description = models.CharField(
        max_length=150,
        default="دارد (همراه اثر)",
        blank=True,
        verbose_name=_("وضعیت شناسنامه فیزیکی (نمایش در شناسنامه فنی)")
    )

    is_approved = models.BooleanField(
        default=True,
        verbose_name=_("تأیید شده توسط مدیر سایت"),
        help_text=_("تنها در صورت تأیید مدیر، محصول در نمای فروشگاه نمایش داده می‌شود.")
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="published",
        verbose_name=_("وضعیت انتشار")
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("نمایش در بخش آثار برگزیده / ویژه")
    )
    tags = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("برچسب‌ها (با کاما جدا کنید)")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ثبت اثر"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاریخ آخرین ویرایش"))

    class Meta:
        verbose_name = _("محصول و اثر هنری")
        verbose_name_plural = _("محصولات و آثار هنری")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.booth.name} ({self.price:,} تومان)"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def has_discount(self):
        return bool(self.discount_price and self.discount_price < self.price)


class ProductImage(models.Model):
    """گالری تصاویر اضافی محصول"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery_images",
        verbose_name=_("محصول مربوطه")
    )
    image = models.ImageField(upload_to="products/gallery/", verbose_name=_("تصویر گالری"))
    alt_text = models.CharField(max_length=150, blank=True, verbose_name=_("متن جایگزین (Alt)"))

    class Meta:
        verbose_name = _("تصویر گالری")
        verbose_name_plural = _("تصاویر گالری محصول")

    def __str__(self):
        return f"تصویر اضافی برای {self.product.name}"
