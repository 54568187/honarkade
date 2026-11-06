from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.db.models import Q
from unfold.admin import ModelAdmin, StackedInline
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from .models import UserProfile, Customer, StaffUser

# لغو ثبت مدل خام User برای جلوگیری از تداخل و ایجاد ساختار تفکیک‌شده و منظم
if admin.site.is_registered(User):
    admin.site.unregister(User)

if admin.site.is_registered(Group):
    admin.site.unregister(Group)


class CustomerProfileInline(StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = "اطلاعات تماس و نشانی مشتری"
    verbose_name_plural = "اطلاعات تماس و نشانی پستی مشتری"
    fields = ("phone_number", "city", "address", "avatar", "bio")


class StaffUserProfileInline(StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = "مشخصات تکمیلی و جایگاه سازمانی"
    verbose_name_plural = "مشخصات تکمیلی و جایگاه سازمانی"
    fields = ("role", "phone_number", "city", "avatar", "bio")


@admin.register(Customer)
class CustomerAdmin(BaseUserAdmin, ModelAdmin):
    """مدیریت اختصاصی خریداران و مشتریان هنر"""
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    inlines = [CustomerProfileInline]

    list_display = ("username", "get_full_name", "get_phone", "get_city", "date_joined", "is_active")
    list_filter = ("is_active", "date_joined")
    search_fields = ("username", "first_name", "last_name", "email", "profile__phone_number", "profile__city")
    ordering = ("-id",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("اطلاعات فردی و ارتباطی", {"fields": ("first_name", "last_name", "email")}),
        ("وضعیت دسترسی حساب", {"fields": ("is_active",)}),
        ("تاریخچه ثبت‌نام و ورود", {"fields": ("last_login", "date_joined")}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_staff=False, is_superuser=False)

    def get_phone(self, obj):
        if hasattr(obj, "profile") and obj.profile.phone_number:
            return obj.profile.phone_number
        return "-"
    get_phone.short_description = "شماره همراه"

    def get_city(self, obj):
        if hasattr(obj, "profile") and obj.profile.city:
            return obj.profile.city
        return "-"
    get_city.short_description = "شهر"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_staff = False
            obj.is_superuser = False
        super().save_model(request, obj, form, change)
        if hasattr(obj, "profile"):
            obj.profile.role = "customer"
            obj.profile.save()


@admin.register(StaffUser)
class StaffUserAdmin(BaseUserAdmin, ModelAdmin):
    """مدیریت اختصاصی پرسنل، مدیران و کارمندان سامانه"""
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    inlines = [StaffUserProfileInline]

    list_display = ("username", "get_full_name", "email", "get_role", "is_superuser", "is_active", "last_login")
    list_filter = ("is_superuser", "is_active", "profile__role", "groups")
    search_fields = ("username", "first_name", "last_name", "email", "profile__phone_number")
    ordering = ("-id",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(Q(is_staff=True) | Q(is_superuser=True))

    def get_role(self, obj):
        if hasattr(obj, "profile"):
            return obj.profile.get_role_display()
        return "-"
    get_role.short_description = "سمت / نقش سازمانی"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_staff = True
        super().save_model(request, obj, form, change)


@admin.register(Group)
class CustomGroupAdmin(BaseGroupAdmin, ModelAdmin):
    """مدیریت نقش‌ها و مجوزهای دسترسی"""
    search_fields = ("name",)
