from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSetting(models.Model):
    """
    تنظیمات کلی فروشگاه، اطلاعات تماس، لوگو، فاوآیکون و وضعیت نگهداری
    """
    title = models.CharField(
        max_length=200,
        default="هنرکده | گالری و فروشگاه آنلاین آثار هنری و دست‌سازه‌ها",
        verbose_name=_("نام و عنوان فروشگاه")
    )
    tagline = models.CharField(
        max_length=300,
        default="بازار آنلاین هنرمندان، تولیدکنندگان و دوستداران صنایع‌دستی",
        verbose_name=_("شعار فروشگاه")
    )
    email = models.EmailField(
        default="info@kadehonar.ir",
        verbose_name=_("رایانامه (ایمیل) فروشگاه")
    )
    phone = models.CharField(
        max_length=50,
        default="۰۲۱-۸۸۸۸۴۴۴۴",
        verbose_name=_("تلفن تماس")
    )
    address = models.TextField(
        default="تهران، خیابان استاد نجات‌اللهی (ویلا)، پلاک ۱۱۰، ساختمان هنرمندان",
        verbose_name=_("نشانی فیزیکی فروشگاه")
    )
    currency = models.CharField(
        max_length=20,
        default="تومان",
        verbose_name=_("واحد پولی پیش‌فرض")
    )
    
    header_logo = models.ImageField(
        upload_to="settings/logos/",
        blank=True,
        null=True,
        verbose_name=_("نشان تصویری سربرگ (لوگوی سایت)")
    )
    invoice_logo = models.ImageField(
        upload_to="settings/logos/",
        blank=True,
        null=True,
        verbose_name=_("لوگوی ایمیل و برگ‌خرید (فاکتور)")
    )
    favicon = models.ImageField(
        upload_to="settings/logos/",
        blank=True,
        null=True,
        verbose_name=_("فاوآیکون (Favicon)")
    )

    is_maintenance_mode = models.BooleanField(
        default=False,
        verbose_name=_("فعال بودن حالت تعمیرات (تعلیق موقت فروشگاه)")
    )
    maintenance_allowed_ips = models.TextField(
        blank=True,
        default="127.0.0.1, ::1",
        verbose_name=_("آدرس‌های IP مجاز زمان تعمیرات"),
        help_text=_("آدرس‌های IP را با علامت کاما (,) از هم جدا کنید.")
    )
    maintenance_message = models.TextField(
        default="فروشگاه در حال به‌روزرسانی است. به زودی با آثار و دست‌سازه‌های جدید همراه شما خواهیم بود.",
        verbose_name=_("متن سفارشی حالت تعمیرات")
    )

    slider_speed = models.PositiveIntegerField(
        default=7,
        verbose_name=_("سرعت تعویض اسلایدها (ثانیه)")
    )
    slider_stop_at_end = models.BooleanField(
        default=False,
        verbose_name=_("توقف بعد از نمایش آخرین اسلاید")
    )

    # اطلاعات حساب بانکی جهت پرداخت با فیش بانکی (کارگاه ۱۷ کتاب درسی)
    bank_name = models.CharField(
        max_length=100,
        default="بانک ملی ایران",
        verbose_name=_("نام بانک جهت واریز فیش")
    )
    bank_card_number = models.CharField(
        max_length=30,
        default="۶۰۳۷-۹۹۷۵-۱۲۳۴-۵۶۷۸",
        verbose_name=_("شماره کارت بانکی فروشگاه")
    )
    bank_account_number = models.CharField(
        max_length=30,
        default="۰۱۱۴۵۸۷۲۲۹۰۰۱",
        verbose_name=_("شماره حساب بانکی")
    )
    bank_shaba_number = models.CharField(
        max_length=40,
        default="IR540170000000114587229001",
        verbose_name=_("شماره شبا (IBAN)")
    )
    bank_owner_name = models.CharField(
        max_length=100,
        default="فروشگاه صنایع‌دستی و آثار هنری هنرکده",
        verbose_name=_("نام صاحب حساب بانکی")
    )

    footer_copyright = models.CharField(
        max_length=300,
        default="تمامی حقوق مادی و معنوی متعلق به بازارچه آنلاین هنرکده است.",
        verbose_name=_("متن کپی‌رایت پاصفحه (فوتر)")
    )

    # محتوای نمایشی صفحه اصلی و ویترین
    hero_showcase_title = models.CharField(
        max_length=200,
        default="جدیدترین آثار هنری و صنایع‌دستی",
        verbose_name=_("عنوان بخش ویترین صفحه اصلی")
    )
    hero_showcase_subtitle = models.CharField(
        max_length=300,
        default="آثار اصیل با قیمت شفاف، شناسنامه معتبر و ارسال ایمن به تمام نقاط ایران",
        verbose_name=_("توضیحات کوتاه بخش ویترین")
    )

    # ترجمه قالب و عبارات متنی فروشگاه (کارگاه ۱۹ کتاب درسی)
    popular_products_title = models.CharField(
        max_length=150,
        default="محصولات پیشنهادی",
        verbose_name=_("ترجمه عبارت «محصولات پرطرفدار» (Popular Products)"),
        help_text=_("طبق کارگاه ۱۹ کتاب: جایگزین کردن «محصولات پرطرفدار» با «محصولات پیشنهادی» یا «محصولات پرفروش»")
    )
    special_offers_title = models.CharField(
        max_length=150,
        default="پیشنهاد شگفت‌انگیز",
        verbose_name=_("ترجمه عبارت «کاهش قیمت‌ها» (Special Offers)"),
        help_text=_("طبق فعالیت کارگاهی صفحه ۸۸ کتاب: جایگزین کردن «کاهش قیمت‌ها» با «پیشنهاد شگفت‌انگیز»")
    )

    # بنر فراخوان جذب و معرفی هنرمندان در صفحه اصلی
    call_to_action_badge = models.CharField(
        max_length=150,
        default="حمایت از هنرمندان مستقل",
        verbose_name=_("برچسب بالای بنر فراخوان")
    )
    call_to_action_title = models.CharField(
        max_length=255,
        default="هنرمند گرامی، اثر خودت را به هنرکده بسپار",
        verbose_name=_("عنوان بنر فراخوان هنرمندان")
    )
    call_to_action_desc = models.TextField(
        default="عکس و مشخصات اثر خود را ثبت کنید؛ پس از بررسی، اثر با نام شما در ویترین اختصاصی گالری به تمام کشور عرضه می‌شود.",
        verbose_name=_("توضیحات بنر فراخوان هنرمندان")
    )
    call_to_action_btn = models.CharField(
        max_length=100,
        default="فرم ارسال اثر برای بررسی",
        verbose_name=_("متن دکمه بنر فراخوان")
    )
    call_to_action_url = models.CharField(
        max_length=255,
        default="/register/",
        verbose_name=_("آدرس لینک دکمه بنر فراخوان")
    )

    # ۴ مزیت خرید در فوتر سایت
    benefit_1_title = models.CharField(max_length=150, default="شناسنامه و گواهی اصالت", verbose_name=_("تیتر مزیت ۱ فوتر"))
    benefit_1_desc = models.CharField(max_length=250, default="امضای مستقیم هنرمند و گواهی معتبر", verbose_name=_("شرح مزیت ۱ فوتر"))
    benefit_2_title = models.CharField(max_length=150, default="بسته‌بندی تخصصی هنری", verbose_name=_("تیتر مزیت ۲ فوتر"))
    benefit_2_desc = models.CharField(max_length=250, default="ارسال ضدضربه با بیمه کامل مرسوله", verbose_name=_("شرح مزیت ۲ فوتر"))
    benefit_3_title = models.CharField(max_length=150, default="۷ روز ضمانت بازگشت", verbose_name=_("تیتر مزیت ۳ فوتر"))
    benefit_3_desc = models.CharField(max_length=250, default="تضمین سلامت فیزیکی و تطابق اثر", verbose_name=_("شرح مزیت ۳ فوتر"))
    benefit_4_title = models.CharField(max_length=150, default="مشاوره رایگان دکوراسیون", verbose_name=_("تیتر مزیت ۴ فوتر"))
    benefit_4_desc = models.CharField(max_length=250, default="پاسخگویی و هماهنگی کارشناسان گالری", verbose_name=_("شرح مزیت ۴ فوتر"))

    class Meta:
        verbose_name = _("تنظیمات کلی و پیکربندی فروشگاه")
        verbose_name_plural = _("تنظیمات کلی و پیکربندی فروشگاه")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return f"{self.title} (پیکربندی فروشگاه)"


class StaticPage(models.Model):
    """
    صفحات ایستا و راهنما مانند شرایط و ضوابط، درباره ما، روش ارسال و پرداخت امن
    """
    title = models.CharField(max_length=200, verbose_name=_("عنوان صفحه"))
    slug = models.SlugField(
        max_length=200,
        unique=True,
        allow_unicode=True,
        verbose_name=_("URL آشنا (پیوند یکتا)")
    )
    content = models.TextField(verbose_name=_("محتوای متنی صفحه"))
    meta_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("عنوان متا (سئو)")
    )
    meta_description = models.TextField(
        blank=True,
        verbose_name=_("توضیحات متا (سئو)")
    )
    show_in_footer = models.BooleanField(
        default=True,
        verbose_name=_("نمایش در پاصفحه (Footer)")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("وضعیت انتشار"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("ترتیب نمایش"))

    class Meta:
        verbose_name = _("صفحه ایستا")
        verbose_name_plural = _("صفحات ایستا و قوانین")
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Slider(models.Model):
    """
    اسلایدر تصویر صفحه اصلی
    """
    title = models.CharField(max_length=200, verbose_name=_("عنوان اسلاید"))
    subtitle = models.CharField(
        max_length=300,
        blank=True,
        verbose_name=_("توضیحات روی تصویر")
    )
    image = models.ImageField(
        upload_to="slider/",
        verbose_name=_("پرونده تصویر اسلاید")
    )
    link = models.CharField(
        max_length=500,
        default="/shop/",
        verbose_name=_("آدرس صفحه مقصد (لینک)")
    )
    button_text = models.CharField(
        max_length=100,
        default="مشاهده و خرید آثار",
        verbose_name=_("عنوان دکمه")
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("ترتیب نمایش (اولویت)")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("فعال یا غیرفعال بودن اسلاید")
    )

    class Meta:
        verbose_name = _("اسلاید تصویر")
        verbose_name_plural = _("اسلایدر صفحه اصلی")
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.title} (اولویت: {self.order})"


class Banner(models.Model):
    """
    بنرهای تبلیغاتی و اطلاعیه‌ها
    """
    POSITION_CHOICES = (
        ("top", _("بنر باریک بالای صفحه (هدر)")),
        ("middle", _("بنر عریض میانه صفحه")),
        ("sidebar", _("بنر ستون کناری")),
    )
    title = models.CharField(max_length=200, verbose_name=_("عنوان نمایش داده شده"))
    description = models.CharField(
        max_length=400,
        blank=True,
        verbose_name=_("توضیحات روی تصویر / پیام جشنواره")
    )
    image = models.ImageField(
        upload_to="banners/",
        blank=True,
        null=True,
        verbose_name=_("نام پرونده تصویر")
    )
    alt_text = models.CharField(
        max_length=200,
        default="بنر جشنواره هنرکده",
        verbose_name=_("متن جایگزین (Alt)")
    )
    link = models.CharField(
        max_length=500,
        default="/shop/",
        verbose_name=_("آدرس صفحه مقصد")
    )
    discount_code = models.CharField(
        max_length=50,
        blank=True,
        default="HONAR15",
        verbose_name=_("کد تخفیف ویژه بنر")
    )
    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default="top",
        verbose_name=_("موقعیت نمایش بنر")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("فعال بودن بنر"))

    class Meta:
        verbose_name = _("بنر تبلیغاتی")
        verbose_name_plural = _("بنرهای تبلیغاتی")

    def __str__(self):
        return f"{self.title} ({self.get_position_display()})"


class MenuItem(models.Model):
    """
    منوی ناوبری تارنما
    """
    title = models.CharField(max_length=150, verbose_name=_("عنوان آیتم منو"))
    url = models.CharField(max_length=500, verbose_name=_("آدرس پیوند (URL)"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("ترتیب نمایش"))
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("آیتم والد (برای زیرمنو)")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("وضعیت نمایش"))

    class Meta:
        verbose_name = _("آیتم منو")
        verbose_name_plural = _("منوی ناوبری تارنما")
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ThemeTranslation(models.Model):
    """
    سیستم ترجمه و بومی‌سازی قالب فروشگاه (کارگاه ۱۹ پودمان دوم)
    امکان جستجو و جایگزینی عبارات متنی قالب به زبان‌های فارسی و انگلیسی
    """
    SECTION_CHOICES = (
        ("home", _("صفحه اصلی و ویترین‌ها (Home Page)")),
        ("header", _("سربرگ، منو و ناوبری (Header & Navigation)")),
        ("shop", _("فروشگاه و فیلترهای لایه‌ای (Shop & Filters)")),
        ("cart", _("سبد خرید و تسویه‌حساب (Cart & Checkout)")),
        ("footer", _("پاصفحه و نشان‌های اعتماد (Footer & Trust)")),
    )

    key = models.SlugField(max_length=100, unique=True, verbose_name=_("شناسه سیستمی (Key)"))
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default="home", verbose_name=_("بخش قالب"))
    original_phrase = models.CharField(max_length=255, verbose_name=_("عبارت اصلی قالب (پیش‌فرض)"))
    fa_translation = models.CharField(max_length=255, verbose_name=_("جایگزین / ترجمه فارسی (FA)"))
    en_translation = models.CharField(max_length=255, verbose_name=_("ترجمه انگلیسی (EN)"))
    description = models.CharField(max_length=255, blank=True, verbose_name=_("راهنمای کاربرد در قالب"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("آخرین ویرایش"))

    class Meta:
        verbose_name = _("عبارت قالب (ترجمه)")
        verbose_name_plural = _("ترجمه‌ها و عبارات قالب (کارگاه ۱۹)")
        ordering = ["section", "id"]

    def __str__(self):
        return f"{self.original_phrase} ➔ {self.fa_translation} | {self.en_translation}"

