from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect

from .models import Booth, Product
from orders.models import Order, OrderItem, SettlementRequest


def booth_dashboard_view(request):
    """
    داشبورد مستقل و فرانت‌اند غرفه‌داران و هنرمندان (جدا از پنل ادمین جنگو)
    امکان مشاهده سفارش‌های ثبت‌شده مشتریان، اطلاعات مالی و تسویه حساب، و ویرایش شماره شبا و حساب بانکی
    """
    all_booths = Booth.objects.all().order_by("id")
    
    # تعیین غرفه فعال: در صورت لاگین بودن با اکانت صاحب غرفه، یا انتخاب دستی از سوئیچر غرفه‌ها
    booth = None
    if request.user.is_authenticated and hasattr(request.user, "booth"):
        booth = request.user.booth
    
    requested_booth_id = request.GET.get("booth_id") or request.POST.get("booth_id")
    if requested_booth_id:
        booth = Booth.objects.filter(id=requested_booth_id).first()

    if not booth:
        booth = all_booths.first()

    # عملیات POST: ویرایش اطلاعات بانکی، ثبت درخواست تسویه حساب، تغییر وضعیت سفارش
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "update_bank_info" and booth:
            booth.bank_name = request.POST.get("bank_name", "").strip() or booth.bank_name
            booth.bank_account_holder = request.POST.get("bank_account_holder", "").strip() or booth.bank_account_holder
            booth.bank_shaba = request.POST.get("bank_shaba", "").strip() or booth.bank_shaba
            booth.bank_card = request.POST.get("bank_card", "").strip() or booth.bank_card
            booth.bank_account_number = request.POST.get("bank_account_number", "").strip() or booth.bank_account_number
            booth.save()
            messages.success(request, "اطلاعات حساب و شماره شبای بانکی غرفه با موفقیت ذخیره شد.")
            return redirect(f"/booth/dashboard/?booth_id={booth.id}")

        elif action == "request_settlement" and booth:
            amount_str = request.POST.get("amount", "0").replace(",", "").strip()
            amount = int(amount_str) if amount_str.isdigit() else 0
            if amount > 0 and amount <= booth.wallet_balance:
                SettlementRequest.objects.create(
                    booth=booth,
                    amount=amount,
                    shaba_number=booth.bank_shaba,
                    card_number=booth.bank_card,
                    status="pending"
                )
                booth.settlement_status = "pending"
                booth.save(update_fields=["settlement_status"])
                messages.success(request, f"درخواست تسویه حساب به مبلغ {amount:,} تومان با موفقیت ثبت شد و در صف واریز پایا قرار گرفت.")
            else:
                messages.error(request, "مبلغ درخواستی تسویه نامعتبر است یا از موجودی کیف پول بیشتر است.")
            return redirect(f"/booth/dashboard/?booth_id={booth.id}")

        elif action == "update_order_status":
            order_id = request.POST.get("order_id")
            new_status = request.POST.get("new_status")
            if order_id and new_status:
                order = Order.objects.filter(id=order_id).first()
                if order:
                    order.status = new_status
                    order.save(update_fields=["status"])
                    messages.success(request, f"وضعیت سفارش شماره #{order.id} به «{order.get_status_display()}» تغییر یافت.")
            return redirect(f"/booth/dashboard/?booth_id={booth.id}")

    # دریافت سفارش‌های مربوط به آثار این غرفه ("کی درخواست داده برای خرید")
    booth_orders = []
    booth_products = []
    settlement_requests = []

    if booth:
        booth_orders = Order.objects.filter(
            items__product__booth=booth
        ).distinct().select_related("customer", "carrier", "province").prefetch_related("items__product").order_by("-id")

        booth_products = Product.objects.filter(booth=booth)
        settlement_requests = SettlementRequest.objects.filter(booth=booth).order_by("-id")

    context = {
        "all_booths": all_booths,
        "current_booth": booth,
        "booth_orders": booth_orders,
        "booth_products": booth_products,
        "settlement_requests": settlement_requests,
        "total_orders_count": len(booth_orders),
        "total_revenue": sum(o.total_products_price for o in booth_orders),
    }
    return render(request, "pages/booth_dashboard.html", context)
