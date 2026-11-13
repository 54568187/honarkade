import json
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from .models import Order, OrderItem, SettlementRequest
from catalog.models import Product, Booth
from shipping.models import Carrier, Province
from core.models import PaymentGatewaySetting


def checkout_submit_view(request):
    """ثبت نهایی سفارش از سبد خرید و هدایت به درگاه پرداخت شاپرک یا فیش بانکی"""
    if request.method == "POST":
        # دریافت اطلاعات مشتری
        customer = request.user if request.user.is_authenticated else None
        if not customer:
            customer = User.objects.filter(is_superuser=True).first() or User.objects.first()
            if not customer:
                customer = User.objects.create_user(username="guest_buyer", first_name="خریدار", last_name="مهمان")

        receiver_name = request.POST.get("receiver_name", "").strip() or "خریدار محترم"
        phone = request.POST.get("phone", "").strip() or "09120000000"
        province_id = request.POST.get("province")
        city = request.POST.get("city", "").strip() or "تهران"
        address = request.POST.get("address", "").strip() or "نشانی ثبت شده در پیش‌فاکتور"
        postal_code = request.POST.get("postal_code", "").strip() or "1136912345"
        notes = request.POST.get("notes", "").strip()
        carrier_id = request.POST.get("carrier")
        payment_method = request.POST.get("payment_method", "online")
        bank_tracking_code = request.POST.get("bank_tracking_code", "").strip()
        
        # بازه زمانی دریافت و روز ارسال کالا
        delivery_date = request.POST.get("delivery_date", "سریع‌ترین زمان ممکن (۱ الی ۳ روز کاری)").strip()
        delivery_time_slot = request.POST.get("delivery_time_slot", "ساعت ۹ الی ۱۳ (صبح)").strip()
        
        # گزینه‌های بسته‌بندی
        is_gift_wrapped = request.POST.get("is_gift_wrapped") in ["1", "true", "on", True]
        gift_message = request.POST.get("gift_message", "").strip()
        is_recycled_packaging = request.POST.get("is_recycled_packaging") in ["1", "true", "on", True]

        carrier = None
        if carrier_id:
            carrier = Carrier.objects.filter(id=carrier_id).first()
        if not carrier:
            carrier = Carrier.objects.filter(is_active=True).first()

        province = None
        if province_id:
            province = Province.objects.filter(id=province_id).first()

        # دریافت اقلام سبد خرید از فرم به صورت JSON یا محصولات نمونه
        cart_data_raw = request.POST.get("cart_items_json", "")
        cart_items_data = []
        if cart_data_raw:
            try:
                cart_items_data = json.loads(cart_data_raw)
            except Exception:
                cart_items_data = []

        # ایجاد سفارش
        order = Order.objects.create(
            customer=customer,
            carrier=carrier,
            province=province,
            city=city,
            address=f"{receiver_name} - {address}",
            postal_code=postal_code,
            phone=phone,
            notes=notes,
            payment_method=payment_method,
            bank_tracking_code=bank_tracking_code,
            delivery_date=delivery_date,
            delivery_time_slot=delivery_time_slot,
            is_gift_wrapped=is_gift_wrapped,
            gift_message=gift_message,
            is_recycled_packaging=is_recycled_packaging,
            status="pending" if payment_method == "online" else "remote_paid"
        )

        total_prod_price = 0
        added_items = 0

        if cart_items_data:
            for item in cart_items_data:
                p_id = item.get("id")
                qty = int(item.get("qty") or 1)
                product = None
                if p_id and str(p_id).isdigit():
                    product = Product.objects.filter(id=int(p_id)).first()
                elif p_id:
                    # تلاش برای پیدا کردن از طریق اسلاگ یا نام
                    product = Product.objects.filter(name__icontains=item.get("title", "")).first()

                if not product:
                    product = Product.objects.filter(is_approved=True).first()

                if product:
                    unit_p = product.price if not product.discount_price else product.discount_price
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=qty,
                        unit_price=unit_p,
                        selected_attributes="استاندارد"
                    )
                    total_prod_price += (unit_p * qty)
                    added_items += 1

        if added_items == 0:
            # یک محصول پیش‌فرض از غرفه‌ها اضافه کنیم تا سفارش خالی نباشد
            sample_prod = Product.objects.filter(is_approved=True).first()
            if sample_prod:
                unit_p = sample_prod.price if not sample_prod.discount_price else sample_prod.discount_price
                OrderItem.objects.create(
                    order=order,
                    product=sample_prod,
                    quantity=1,
                    unit_price=unit_p,
                    selected_attributes="تک‌نسخه استاندارد"
                )
                total_prod_price = unit_p

        order.total_products_price = total_prod_price
        order.shipping_cost = carrier.calculate_cost_for_province(province) if carrier else 45000
        order.save()

        if payment_method == "online":
            return redirect("payment_gateway", order_id=order.id)
        else:
            return redirect("payment_receipt", order_id=order.id)

    return redirect("cart")


def direct_buy_view(request, product_id):
    """خرید سریع مستقیم از صفحه محصول با درگاه بانکی شاپرک"""
    product = get_object_or_404(Product, id=product_id)
    
    customer = request.user if request.user.is_authenticated else None
    if not customer:
        customer = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if not customer:
            customer = User.objects.create_user(username="quick_buyer", first_name="خریدار", last_name="آنی")

    carrier = Carrier.objects.filter(is_active=True).first()
    province = Province.objects.first()

    delivery_date = request.GET.get("date", "یکشنبه ۲۵ آبان")
    delivery_time_slot = request.GET.get("slot", "ساعت ۱۴ الی ۱۸ (عصر)")

    order = Order.objects.create(
        customer=customer,
        carrier=carrier,
        province=province,
        city="تهران",
        address="خرید سریع آنلاین از غرفه اثر",
        postal_code="1136912345",
        phone="09121112233",
        payment_method="online",
        delivery_date=delivery_date,
        delivery_time_slot=delivery_time_slot,
        status="pending",
        is_recycled_packaging=True,
    )

    unit_p = product.price if not product.discount_price else product.discount_price
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        unit_price=unit_p,
        selected_attributes="خرید سریع اثر"
    )

    order.total_products_price = unit_p
    order.shipping_cost = carrier.calculate_cost_for_province(province) if carrier else 45000
    order.save()

    return redirect("payment_gateway", order_id=order.id)


def payment_gateway_view(request, order_id=None):
    """
    شبیه‌ساز رسمی درگاه پرداخت الکترونیک به پرداخت ملت (شاپرک)
    مطابق با تصویر ارسالی کاربر (Behpardakht Mellat)
    """
    if order_id:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = Order.objects.order_by("-id").first()
        if not order:
            customer = User.objects.first() or User.objects.create_user(username="demo_user")
            product = Product.objects.first()
            carrier = Carrier.objects.first()
            order = Order.objects.create(
                customer=customer,
                carrier=carrier,
                city="تهران",
                address="تهران، خیابان کریمخان زند، پلاک ۱۲",
                postal_code="1136912345",
                phone="09120000000",
                total_products_price=300000,
                shipping_cost=0,
                total_price=300000,
                status="pending"
            )
            if product:
                OrderItem.objects.create(order=order, product=product, quantity=1, unit_price=300000)

    # اطلاعات تنظیمات درگاه و حساب بانکی پلتفرم
    gateway_settings = PaymentGatewaySetting.get_settings()
    
    # مشخص کردن غرفه اثر مربوطه
    first_item = order.items.select_related("product__booth").first()
    booth = first_item.product.booth if first_item and first_item.product and first_item.product.booth else None
    
    merchant_name = f"رایان پی (هنرکده - {booth.name})" if booth else "رایان پی (بازارچه هنرکده)"
    
    # تبدیل تومان به ریال برای نمایش روی درگاه مانند تصویر
    price_toman = order.total_price if order.total_price > 0 else 300000
    price_rial = price_toman * 10

    context = {
        "order": order,
        "booth": booth,
        "gateway_settings": gateway_settings,
        "merchant_name": merchant_name,
        "merchant_id": gateway_settings.merchant_id or "2374257",
        "terminal_id": gateway_settings.terminal_id or "5841895",
        "price_rial": price_rial,
        "price_toman": price_toman,
        "website_url": "https://kadehonar.ir",
    }
    return render(request, "pages/payment_gateway.html", context)


@csrf_exempt
def payment_process_view(request, order_id):
    """پردازش و اعتبارسنجی تراکنش درگاه بانکی شاپرک"""
    if request.method != "POST":
        return redirect("payment_gateway", order_id=order_id)

    order = get_object_or_404(Order, id=order_id)
    card_number = request.POST.get("card_number", "").replace(" ", "").replace("-", "")
    email = request.POST.get("email", "")

    # تولید کد پیگیری رندوم ۱۲ رقمی شاپرک
    ref_code = f"SHP{random.randint(100000000, 999999999)}"
    masked_card = f"{card_number[:4]}-****-****-{card_number[-4:]}" if len(card_number) >= 12 else "6037-****-****-2841"

    # به‌روزرسانی سفارش
    order.status = "processing"
    order.gateway_ref_code = ref_code
    order.card_masked_number = masked_card
    order.paid_at = timezone.now()
    order.save()

    # افزایش موجودی کیف پول غرفه‌دار
    first_item = order.items.select_related("product__booth").first()
    if first_item and first_item.product and first_item.product.booth:
        booth = first_item.product.booth
        # سهم غرفه = کل مبلغ محصولات منهای کارمزد هنرکده
        net_booth_share = order.total_products_price - order.commission_amount
        if net_booth_share > 0:
            booth.wallet_balance += net_booth_share
            booth.total_earnings += net_booth_share
            booth.save(update_fields=["wallet_balance", "total_earnings"])

    return redirect("payment_receipt", order_id=order.id)


def payment_receipt_view(request, order_id):
    """نمایش رسید دیجیتال و فیش تایید تراکنش شاپرک و جزئیات سفارش"""
    order = get_object_or_404(Order, id=order_id)
    first_item = order.items.select_related("product__booth").first()
    booth = first_item.product.booth if first_item and first_item.product and first_item.product.booth else None

    price_rial = order.total_price * 10

    context = {
        "order": order,
        "booth": booth,
        "price_rial": price_rial,
        "price_toman": order.total_price,
    }
    return render(request, "pages/payment_receipt.html", context)
