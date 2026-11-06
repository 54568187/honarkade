from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Region, Province, Carrier


@admin.register(Region)
class RegionAdmin(ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Province)
class ProvinceAdmin(ModelAdmin):
    list_display = ("name", "region", "is_active")
    list_editable = ("region", "is_active")
    list_filter = ("region", "is_active")
    search_fields = ("name",)


@admin.register(Carrier)
class CarrierAdmin(ModelAdmin):
    list_display = ("name", "transit_time", "weight_range_display", "cost_native", "cost_neighbor", "cost_non_neighbor", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name",)
    
    fieldsets = (
        ("مشخصات حامل و کانال توزیع", {
            "fields": ("name", "transit_time", "min_weight", "max_weight", "is_active"),
            "description": "تعریف روش ارسال پستی یا باربری و محدوده وزن مجاز."
        }),
        ("تعرفه‌های حمل بر اساس منطقه‌بندی", {
            "fields": ("cost_native", "cost_neighbor", "cost_non_neighbor"),
            "description": "هزینه ارسال به استان بومی، استان‌های همجوار و استان‌های غیرهمجوار."
        }),
    )

    def weight_range_display(self, obj):
        return f"{obj.min_weight} تا {obj.max_weight} گرم"
    weight_range_display.short_description = "دامنه وزن مجاز"
