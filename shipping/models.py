from django.db import models
from django.utils.translation import gettext_lazy as _


class Region(models.Model):
    """منطقه‌های جغرافیایی جهت تعرفه‌گذاری ارسال"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("نام منطقه (مانند استان بومی، استان همجوار)")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("توضیحات شرایط منطقه")
    )

    class Meta:
        verbose_name = _("منطقه")
        verbose_name_plural = _("منطقه‌های حمل‌ونقل و توزیع")

    def __str__(self):
        return self.name


class Province(models.Model):
    """استان‌های کشور ایران"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("نام استان")
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="provinces",
        verbose_name=_("منطقه توزیع مربوطه")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("فعال بودن ارسال به این استان")
    )

    class Meta:
        verbose_name = _("استان")
        verbose_name_plural = _("استان‌های تحت پوشش")
        ordering = ["name"]

    def __str__(self):
        region_str = f" ({self.region.name})" if self.region else ""
        return f"{self.name}{region_str}"


class Carrier(models.Model):
    """حامل‌ها و روش‌های ارسال سفارشات"""
    name = models.CharField(
        max_length=150,
        verbose_name=_("نام حامل (مانند پست پیشتاز، تیپاکس، پیک)")
    )
    transit_time = models.CharField(
        max_length=150,
        default="۲ الی ۴ روز کاری",
        verbose_name=_("مدت زمان تحویل مرسوله")
    )
    min_weight = models.PositiveIntegerField(
        default=0,
        verbose_name=_("حداقل وزن مرسوله (گرم)")
    )
    max_weight = models.PositiveIntegerField(
        default=5000,
        verbose_name=_("حداکثر وزن مرسوله (گرم)"),
        help_text=_("برای مثال: حداکثر تا ۵۰۰۰ گرم (۵ کیلوگرم)")
    )
    
    cost_native = models.PositiveIntegerField(
        default=35000,
        verbose_name=_("هزینه ارسال به منطقه بومی (تومان)")
    )
    cost_neighbor = models.PositiveIntegerField(
        default=45000,
        verbose_name=_("هزینه ارسال به استان‌های همجوار (تومان)")
    )
    cost_non_neighbor = models.PositiveIntegerField(
        default=60000,
        verbose_name=_("هزینه ارسال به استان‌های غیرهمجوار (تومان)")
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("فعال بودن این روش ارسال")
    )

    class Meta:
        verbose_name = _("حامل (روش ارسال)")
        verbose_name_plural = _("حامل‌ها و روش‌های ارسال")

    def __str__(self):
        return f"{self.name} (دامنه وزن: {self.min_weight} تا {self.max_weight} گرم)"

    def calculate_cost_for_province(self, province):
        if not province or not province.region:
            return self.cost_native
        
        region_name = province.region.name
        if "بومی" in region_name:
            return self.cost_native
        elif "همجوار" in region_name and "غیر" not in region_name:
            return self.cost_neighbor
        else:
            return self.cost_non_neighbor
