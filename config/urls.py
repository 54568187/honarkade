"""
URL configuration for Honarkadeh project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from core.views import (
    home_view,
    shop_view,
    product_detail_view,
    artists_view,
    cart_view,
    search_view,
    static_page_view,
    login_view,
    register_view,
    logout_view,
    profile_view,
)

urlpatterns = [
    # پنل مدیریت حرفه‌ای و جامع
    path("admin/", admin.site.urls),
    
    # صفحات فروشگاه و بازارچه آنلاین
    path("", home_view, name="home"),
    path("shop/", shop_view, name="shop"),
    path("product/<str:slug>/", product_detail_view, name="product_detail"),
    path("artists/", artists_view, name="artists"),
    path("cart/", cart_view, name="cart"),
    path("search/", search_view, name="search"),
    path("page/<str:slug>/", static_page_view, name="static_page"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("dashboard/", profile_view, name="dashboard"),
]

from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
