from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from core.models import SiteSetting, StaticPage, Slider, Banner, MenuItem
from shipping.models import Region, Province, Carrier
from catalog.models import Category, Attribute, AttributeValue, Feature, FeatureValue, Brand, Supplier, Booth, Product


class Command(BaseCommand):
    help = "راه‌اندازی داده‌های اولیه و تست فروشگاه و بازارچه هنرکده"

    def handle(self, *args, **options):
        # ۱. ساخت سوپریوزر مدیر کل
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@kadehonar.ir",
                "first_name": "مدیر کل",
                "last_name": "سامانه",
                "is_staff": True,
                "is_superuser": True,
            }
        )
        if created:
            admin_user.set_password("admin1234")
            admin_user.save()

        # ۲. ایجاد گروه‌ها و نقش‌های سازمانی
        group_dev, _ = Group.objects.get_or_create(name="توسعه‌دهنده فنی")
        group_seller, _ = Group.objects.get_or_create(name="مدیریت کاتالوگ و محصولات")
        group_support, _ = Group.objects.get_or_create(name="پشتیبانی و امور سفارشات")

        dev_permissions = Permission.objects.filter(
            content_type__app_label__in=["core", "shipping", "catalog"]
        )
        group_dev.permissions.set(dev_permissions)

        seller_permissions = Permission.objects.filter(
            content_type__app_label="catalog"
        )
        group_seller.permissions.set(seller_permissions)

        # ۳. ایجاد کارمند نمونه با نمایه توسعه‌دهنده
        staff_user, s_created = User.objects.get_or_create(
            username="dev_staff",
            defaults={
                "email": "developer@kadehonar.ir",
                "first_name": "مبینا",
                "last_name": "فرهمند",
                "is_staff": True,
            }
        )
        if s_created:
            staff_user.set_password("staff1234")
            staff_user.groups.add(group_dev)
            staff_user.save()
            if hasattr(staff_user, "profile"):
                staff_user.profile.role = "developer"
                staff_user.profile.phone_number = "۰۹۱۲۱۱۱۱۱۱۱"
                staff_user.profile.save()

        # ۴. تنظیمات کلی فروشگاه
        settings = SiteSetting.load()
        settings.title = "هنرکده | گالری و فروشگاه آنلاین آثار هنری و دست‌سازه‌ها"
        settings.tagline = "خرید مستقیم از هنرمندان و تولیدکنندگان مستقل صنایع‌دستی ایران"
        settings.email = "info@kadehonar.ir"
        settings.phone = "۰۲۱-۸۸۸۸۴۴۴۴"
        settings.address = "تهران، خیابان نجات‌اللهی (ویلا)، کوچه هنرمندان، پلاک ۱۲"
        settings.currency = "تومان"
        settings.is_maintenance_mode = False
        settings.maintenance_allowed_ips = "127.0.0.1, ::1"
        settings.maintenance_message = "فروشگاه هنرکده در حال به‌روزرسانی است. به زودی با آثار و دست‌سازه‌های جدید همراه شما خواهیم بود."
        settings.slider_speed = 7
        settings.slider_stop_at_end = False
        settings.footer_copyright = "تمامی حقوق مادی و معنوی متعلق به بازارچه آنلاین هنرکده است."
        settings.save()

        # ۵. صفحات ایستا و قوانین
        pages_data = [
            {
                "title": "درباره هنرکده",
                "slug": "about-us",
                "content": "هنرکده پلتفرمی مستقل برای حمایت از هنرمندان بومی، طراحان و تولیدکنندگان دست‌سازه‌های اصیل ایرانی است. ما پلی مستقیم میان کارگاه هنرمندان و خانه‌های شما هستیم.",
                "meta_title": "درباره گالری و بازارچه هنرکده",
                "meta_description": "آشنایی با داستان پیدایش هنرکده و حمایت از هنرمندان مستقل ایران",
                "order": 1,
            },
            {
                "title": "شرایط و ضوابط استفاده",
                "slug": "terms",
                "content": "استفاده از خدمات هنرکده به منزله پذیرش تمامی قوانین خرید، حقوق مالکیت فکری آثار و ضمانت اصالت کالا می‌باشد. هرگونه کپی‌برداری غیرمجاز از طرح آثار پیگرد قانونی دارد.",
                "meta_title": "قوانین و مقررات خرید از هنرکده",
                "meta_description": "شرایط و ضوابط خرید آثار هنری و ضمانت بازگشت کالا",
                "order": 2,
            },
            {
                "title": "روش‌های ارسال و تحویل",
                "slug": "shipping-methods",
                "content": "تمام آثار به دلیل ظرافت و ارزش هنری با بسته‌بندی پنج‌لایه ضربه‌گیر و بیمه ارزش ارسال می‌شوند. ارسال به سراسر کشور از طریق پست پیشتاز و تیپاکس با کد رهگیری لحظه‌ای صورت می‌گیرد.",
                "meta_title": "روش‌های بسته‌بندی ایمن و ارسال پستی آثار",
                "meta_description": "راهنمای حمل و نقل و هزینه‌های ارسال سفارشی در هنرکده",
                "order": 3,
            },
            {
                "title": "پرداخت امن",
                "slug": "secure-payment",
                "content": "تمامی تراکنش‌های بانکی در هنرکده از طریق درگاه‌های شاپرک رسمی و با پروتکل‌های رمزنگاری شده امن صورت می‌پذیرد.",
                "meta_title": "پرداخت امن و تضمین اصالت تراکنش‌ها",
                "meta_description": "اطلاعات درگاه پرداخت و پروتکل‌های امنیتی بازارچه",
                "order": 4,
            },
            {
                "title": "تماس با ما",
                "slug": "contact-us",
                "content": "کاربران گرامی در صورت داشتن هرگونه سوال درباره وضعیت سفارش یا ثبت غرفه می‌توانند با شماره ۰۲۱-۸۸۸۸۴۴۴۴ یا ایمیل info@kadehonar.ir در ارتباط باشند.",
                "meta_title": "ارتباط با پشتیبانی هنرکده",
                "meta_description": "شماره تماس و نشانی دفتر مرکزی هنرکده",
                "order": 5,
            },
        ]
        for p_data in pages_data:
            StaticPage.objects.get_or_create(slug=p_data["slug"], defaults=p_data)

        # ۶. اسلایدرهای صفحه اصلی
        sliders_data = [
            {
                "title": "اصالت هنر، در خلوت خانه شما",
                "subtitle": "مجموعه‌ای بی‌نظیر از نقاشی‌های آبرنگ و رنگ‌روغن معاصر با امضای مستقیم هنرمندان مستقل و گواهی اصالت فیزیکی.",
                "image": "hero/slide-1.jpg",
                "link": "/shop/?cat=painting",
                "button_text": "مشاهده گالری آثار",
                "order": 1,
            },
            {
                "title": "روح خاک و آتش در دستان هنرمند",
                "subtitle": "ظروف، ماگ‌ها و مجسمه‌های سرامیکی با لعاب‌های ویژه و فرم‌های ارگانیک، ساخته شده با عشق و صبوری.",
                "image": "hero/slide-2.jpg",
                "link": "/shop/?cat=pottery",
                "button_text": "خرید دست‌سازه‌ها",
                "order": 2,
            },
            {
                "title": "کلام فاخر، نقش مانا",
                "subtitle": "تابلوهای نقاشی‌خط و کتیبه‌های نستعلیق از اشعار حافظ، مولانا و سعدی بر بوم و کاغذ دست‌ساز آهارمهره.",
                "image": "hero/slide-3.jpg",
                "link": "/shop/?cat=calligraphy",
                "button_text": "مشاهده آثار خطاطی",
                "order": 3,
            },
        ]
        for s_data in sliders_data:
            Slider.objects.get_or_create(title=s_data["title"], defaults=s_data)

        # ۷. بنر صفحه اصلی
        Banner.objects.get_or_create(
            position="top",
            defaults={
                "title": "جشنواره گالری هنرکده",
                "description": "ارسال رایگان به سراسر کشور + ۱۵٪ تخفیف اولین خرید آثار هنری با کد تخفیف",
                "discount_code": "HONAR15",
                "alt_text": "بنر جشنواره هنرکده و تخفیف آثار",
                "link": "/shop/",
                "is_active": True,
            }
        )

        # ۸. منطقه‌بندی، استان‌ها و روش‌های ارسال
        region_native, _ = Region.objects.get_or_create(
            name="استان بومی",
            defaults={"description": "استان محل فعالیت انبار مرکزی (تهران و البرز)"}
        )
        region_neighbor, _ = Region.objects.get_or_create(
            name="استان‌های همجوار",
            defaults={"description": "استان‌های متصل و هم‌مرز"}
        )
        region_non_neighbor, _ = Region.objects.get_or_create(
            name="استان‌های غیرهمجوار",
            defaults={"description": "سایر استان‌های کشور"}
        )

        provinces = [
            ("تهران", region_native),
            ("البرز", region_native),
            ("قم", region_neighbor),
            ("مرکزی", region_neighbor),
            ("مازندران", region_neighbor),
            ("قزوین", region_neighbor),
            ("اصفهان", region_non_neighbor),
            ("فارس", region_non_neighbor),
            ("خراسان رضوی", region_non_neighbor),
            ("آذربایجان شرقی", region_non_neighbor),
            ("یزد", region_non_neighbor),
            ("گیلان", region_non_neighbor),
            ("خوزستان", region_non_neighbor),
            ("کرمان", region_non_neighbor),
        ]
        for p_name, p_region in provinces:
            Province.objects.get_or_create(name=p_name, defaults={"region": p_region, "is_active": True})

        Carrier.objects.get_or_create(
            name="پست پیشتاز جمهوری اسلامی ایران",
            defaults={
                "transit_time": "۲ الی ۳ روز کاری",
                "min_weight": 0,
                "max_weight": 5000,
                "cost_native": 35000,
                "cost_neighbor": 45000,
                "cost_non_neighbor": 60000,
                "is_active": True,
            }
        )
        Carrier.objects.get_or_create(
            name="تیپاکس اکسپرس (تحویل درب منزل با بیمه شکستنی)",
            defaults={
                "transit_time": "۲۴ الی ۴۸ ساعت",
                "min_weight": 0,
                "max_weight": 20000,
                "cost_native": 55000,
                "cost_neighbor": 70000,
                "cost_non_neighbor": 90000,
                "is_active": True,
            }
        )

        # ۹. شاخه‌ها و دسته‌بندی‌ها
        cat_handicraft, _ = Category.objects.get_or_create(
            slug="handicrafts",
            defaults={
                "name": "صنایع‌دستی",
                "description": "انواع آثار دست‌ساز سنتی و اصیل ایرانی",
                "meta_title": "خرید آنلاین انواع صنایع‌دستی اصیل",
                "order": 1,
            }
        )
        cat_woven, _ = Category.objects.get_or_create(
            slug="woven-products",
            defaults={
                "name": "محصولات دستباف",
                "description": "منسوجات، گلیم‌ها و بافته‌های دست‌دوز اصیل",
                "meta_title": "محصولات دستباف سنتی ایران",
                "order": 2,
            }
        )
        Category.objects.get_or_create(
            slug="ghalamkar-fabrics",
            defaults={
                "name": "پارچه قلمکار",
                "parent": cat_woven,
                "description": "سفره‌ها و رومیزی‌های قلمکار چاپ دستی سنتی اصفهان",
                "order": 1,
            }
        )
        Category.objects.get_or_create(
            slug="termeh-products",
            defaults={
                "name": "محصولات ترمه",
                "parent": cat_woven,
                "description": "ترمه‌های ابریشمی و سرمه‌دوزی شده یزد",
                "order": 2,
            }
        )
        cat_pottery, _ = Category.objects.get_or_create(
            slug="pottery",
            defaults={"name": "سفال و سرامیک", "description": "ظروف و گلدان‌های سرامیکی لعاب‌دار", "order": 3}
        )
        cat_painting, _ = Category.objects.get_or_create(
            slug="painting",
            defaults={"name": "نقاشی و نگارگری", "description": "تابلوهای رنگ‌روغن، آبرنگ و مینیاتور", "order": 4}
        )
        cat_calligraphy, _ = Category.objects.get_or_create(
            slug="calligraphy",
            defaults={"name": "خوشنویسی و خطاطی", "description": "کتیبه‌ها و خط‌نوشته‌های نستعلیق و شکسته", "order": 5}
        )

        # ۱۰. منوی ناوبری تارنما
        menu_items = [
            ("صفحه اصلی", "/", 1),
            ("گالری جامع آثار", "/shop/", 2),
            ("محصولات دستباف", "/shop/?cat=woven-products", 3),
            ("صنایع‌دستی و سرامیک", "/shop/?cat=handicrafts", 4),
            ("غرفه‌های هنرمندان", "/artists/", 5),
            ("درباره هنرکده", "/page/about-us/", 6),
            ("تماس با ما", "/page/contact-us/", 7),
        ]
        for m_title, m_url, m_order in menu_items:
            MenuItem.objects.get_or_create(title=m_title, defaults={"url": m_url, "order": m_order, "is_active": True})

        # ۱۱. مشخصه‌های متغیر (سایز و رنگ)
        attr_size, _ = Attribute.objects.get_or_create(
            name="سایز",
            defaults={"public_name": "اندازه و سایز اثر", "attribute_type": "select"}
        )
        for s_val in ["بزرگ", "متوسط", "کوچک"]:
            AttributeValue.objects.get_or_create(attribute=attr_size, value=s_val)

        attr_color, _ = Attribute.objects.get_or_create(
            name="رنگ",
            defaults={"public_name": "رنگ‌بندی اثر", "attribute_type": "color"}
        )
        colors = [("سفید", "#FFFFFF"), ("آبی فیروزه‌ای", "#00A896"), ("قرمز لاکی", "#B80000"), ("سبز زیتونی", "#2C4A3E")]
        for c_val, c_code in colors:
            AttributeValue.objects.get_or_create(attribute=attr_color, value=c_val, defaults={"color_code": c_code})

        # ۱۲. ویژگی‌های فنی (بافت و جنس)
        feat_texture, _ = Feature.objects.get_or_create(name="بافت")
        for t_val in ["کتان", "پارچه‌ای", "ابریشمی", "پشمی"]:
            FeatureValue.objects.get_or_create(feature=feat_texture, value=t_val)

        feat_material, _ = Feature.objects.get_or_create(name="جنس بدنه")
        for m_val in ["گل رس کائولن با پخت ۱۱۰۰ درجه", "چوب گردوی کهنسال", "کاغذ آهارمهره دست‌ساز"]:
            FeatureValue.objects.get_or_create(feature=feat_material, value=m_val)

        # ۱۳. برندها و نشان‌های تجاری
        brand_souvenir, _ = Brand.objects.get_or_create(
            name="ایران سوغاتی",
            defaults={
                "description": "برند نام‌آشنای تولید و گردآوری سوغات و صنایع‌دستی فاخر ایران",
                "admin_address": "اصفهان، میدان نقش جهان، بازار مسگرها، پلاک ۴۴",
                "admin_phone": "۰۳۱-۳۲۲۲۴۴۵۵",
                "is_active": True,
            }
        )

        # ۱۴. تأمین‌کنندگان
        Supplier.objects.get_or_create(
            name="تعاونی صنایع‌دستی نقش‌جهان اصفهان",
            defaults={
                "contact_person": "استاد احمدی",
                "phone": "۰۹۱۳۲۲۲۴۴۱۱",
                "address": "اصفهان، خیابان سپه",
                "description": "تأمین‌کننده سفره‌های قلمکار و ترمه اصیل",
            }
        )

        # ۱۵. غرفه هنرمندان و محصولات نمونه
        artist_user, _ = User.objects.get_or_create(
            username="artist_kohan",
            defaults={
                "first_name": "سهراب",
                "last_name": "کهن‌زاد",
                "email": "artist@kadehonar.ir",
                "is_staff": False,
            }
        )
        if hasattr(artist_user, "profile"):
            artist_user.profile.role = "seller"
            artist_user.profile.save()

        booth, _ = Booth.objects.get_or_create(
            slug="kohan-studio",
            defaults={
                "name": "آتلیه و استودیو کهن",
                "owner": artist_user,
                "bio": "خلق آثار سرامیکی و نقاشی با الهام از طبیعت و فرم‌های کهن ایرانی.",
                "is_approved": True,
            }
        )

        sample_products = [
            {
                "name": "گلدان سرامیکی فیروزه‌ای با اسلیمی زرنگار",
                "slug": "turquoise-ceramic-vase",
                "category": cat_pottery,
                "price": 1450000,
                "discount_price": 1250000,
                "stock": 3,
                "weight": 850,
                "sku": "CER-001",
                "short_description": "سفال دست‌ساز لعاب فیروزه‌ای با نقوش اسلیمی طلای ۱۲ عیار.",
                "description": "این اثر نفیس توسط استاد کهن‌زاد در کوره حرارت ۱۱۸۰ درجه پخته شده و کاملاً ضدآب و قابل شستشو می‌باشد.",
                "is_approved": True,
                "is_featured": True,
                "image": "products/product-1.jpg",
                "tags": "سرامیک, گلدان, فیروزه, دست‌ساز",
            },
            {
                "name": "تابلو رنگ‌روغن منظره کوهستان الوند",
                "slug": "alvand-mountain-oil-painting",
                "category": cat_painting,
                "price": 3800000,
                "discount_price": None,
                "stock": 1,
                "weight": 1400,
                "sku": "PNT-002",
                "short_description": "نقاشی اصیل با تکنیک کاردک بر روی بوم کتان اعلا در ابعاد ۶۰ در ۹۰ سانتیمتر.",
                "description": "تابلوی نقاشی رنگ‌روغن با امضای هنرمند و دارای گواهی شناسنامه فیزیکی اصالت اثر.",
                "is_approved": True,
                "is_featured": True,
                "image": "products/product-2.jpg",
                "tags": "نقاشی, بوم, منظره, رنگ‌روغن",
            },
            {
                "name": "کتیبه نستعلیق «جانِ جانان» بر کاغذ آهارمهره",
                "slug": "jane-janan-calligraphy",
                "category": cat_calligraphy,
                "price": 2200000,
                "discount_price": 1950000,
                "stock": 2,
                "weight": 600,
                "sku": "CAL-003",
                "short_description": "خوشنویسی اصیل با مرکب سنتی و تذهیب حاشیه طلایی.",
                "description": "اثر فاخر خطاطی شکسته نستعلیق از غزل حضرت حافظ با پاسپارتو دوبل هلندی.",
                "is_approved": True,
                "is_featured": True,
                "image": "products/product-3.jpg",
                "tags": "خوشنویسی, نستعلیق, حافظ, تذهیب",
            },
            {
                "name": "سفره قلمکار اصفهان طرح چهارفصل ابریشمی",
                "slug": "ghalamkar-tablecloth-esfahan",
                "category": cat_woven,
                "brand": brand_souvenir,
                "price": 890000,
                "discount_price": None,
                "stock": 10,
                "weight": 450,
                "sku": "WVN-004",
                "short_description": "چاپ سنتی با قالب‌های چوبی گلابی بر روی پارچه کتان طبیعی ۱۰۰٪ پنبه.",
                "description": "سفره قلمکار درجه یک صادراتی با رنگ‌های طبیعی و ثبات رنگ تضمین شده در برابر شستشو.",
                "is_approved": True,
                "is_featured": True,
                "image": "products/product-4.jpg",
                "tags": "قلمکار, اصفهان, دستباف, رومیزی",
            },
        ]

        for p_data in sample_products:
            p_img = p_data.pop("image")
            brand = p_data.pop("brand", None)
            prod, p_created = Product.objects.get_or_create(
                slug=p_data["slug"],
                defaults={
                    **p_data,
                    "booth": booth,
                    "brand": brand,
                    "image": p_img,
                }
            )
            if p_created:
                prod.attributes.add(*AttributeValue.objects.filter(attribute=attr_size))
                prod.features.add(*FeatureValue.objects.filter(feature=feat_texture))
