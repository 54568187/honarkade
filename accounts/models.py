from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """مشخصات تکمیلی کاربر و جایگاه سازمانی"""
    ROLE_CHOICES = (
        ("admin", _("مدیر ارشد (دسترسی کامل به سامانه)")),
        ("developer", _("توسعه‌دهنده فنی و پشتیبان زیرساخت")),
        ("seller", _("هنرمند و صاحب غرفه (فروشنده)")),
        ("support", _("کارشناس امور مشتریان و سفارشات")),
        ("customer", _("خریدار و مجموعه‌دار هنر")),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("حساب کاربری")
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer",
        verbose_name=_("نقش و جایگاه سازمانی")
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("شماره تلفن همراه")
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name=_("تصویر نمایه (آواتار)")
    )
    bio = models.TextField(
        blank=True,
        verbose_name=_("بیوگرافی / تخصص هنری")
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name=_("شهر محل سکونت")
    )
    address = models.TextField(
        blank=True,
        default="",
        verbose_name=_("نشانی دقیق پستی")
    )

    class Meta:
        verbose_name = _("پروفایل کاربر / کارمند")
        verbose_name_plural = _("پروفایل‌های کاربری")

    def __str__(self):
        full_name = self.user.get_full_name() or self.user.username
        return f"{full_name} - {self.get_role_display()}"


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        role = "admin" if instance.is_superuser else ("seller" if instance.is_staff else "customer")
        UserProfile.objects.get_or_create(user=instance, defaults={"role": role})


class Customer(User):
    """مدل پراکسی اختصاصی مشتریان و خریداران هنر"""
    class Meta:
        proxy = True
        app_label = "accounts"
        verbose_name = _("مشتری / خریدار هنر")
        verbose_name_plural = _("مشتریان و خریداران")


class StaffUser(User):
    """مدل پراکسی اختصاصی پرسنل، مدیران و کارمندان سامانه"""
    class Meta:
        proxy = True
        app_label = "accounts"
        verbose_name = _("کارمند / مدیر سامانه")
        verbose_name_plural = _("پرسنل و کارمندان سامانه")

