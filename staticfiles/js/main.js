/**
 * Honarkadeh Main JavaScript
 * هندل کردن اسلایدر اتوماتیک، مگامنو، سبد خرید پویا، نوتیفیکیشن، تب‌های دسته‌بندی و کلیک کارت‌ها
 */

document.addEventListener('DOMContentLoaded', () => {
  // ================= 1. بنر تبلیغاتی بالای صفحه =================
  const topBanner = document.getElementById('top-banner');
  const closeBannerBtn = document.getElementById('close-banner-btn');
  if (closeBannerBtn && topBanner) {
    closeBannerBtn.addEventListener('click', () => {
      topBanner.style.display = 'none';
    });
  }

  // ================= 2. نوتیفیکیشن / اعلان‌ها =================
  const notifBtn = document.getElementById('notif-btn');
  const notifDropdown = document.getElementById('notif-dropdown');
  if (notifBtn && notifDropdown) {
    notifBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      notifDropdown.classList.toggle('hidden');
    });
    document.addEventListener('click', (e) => {
      if (!notifDropdown.contains(e.target) && !notifBtn.contains(e.target)) {
        notifDropdown.classList.add('hidden');
      }
    });
  }

  // ================= 3. سبد خرید به صورت دراپ‌داون اختصاصی زیر آیکون فروشگاه =================
  const cartBtn = document.getElementById('cart-dropdown-btn') || document.getElementById('cart-drawer-btn') || document.getElementById('cart-btn');
  const cartDropdown = document.getElementById('cart-dropdown-menu') || document.getElementById('cart-dropdown');
  const closeCartBtn = document.getElementById('close-cart-dropdown-btn') || document.getElementById('close-cart-btn');
  const cartBadge = document.getElementById('cart-count-badge');
  const cartDropdownBadge = document.getElementById('cart-items-count-badge');
  const totalPriceEl = document.getElementById('cart-dropdown-total-price');
  const cartItemsContainer = document.getElementById('cart-items-container');

  // توابع تبدیل و فرمت‌بندی اعداد فارسی
  function toFarsiDigits(num) {
    if (num === null || num === undefined) return '';
    const farsiDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    return num.toString().replace(/\d/g, d => farsiDigits[d]);
  }

  function parseFarsiDigits(str) {
    if (!str) return 0;
    const farsiDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    let res = str.toString();
    for (let i = 0; i < 10; i++) {
      res = res.replaceAll(farsiDigits[i], i.toString());
    }
    return parseInt(res.replace(/[^\d]/g, ''), 10) || 0;
  }

  function formatPrice(num) {
    if (!num) return '۰';
    return toFarsiDigits(num.toLocaleString('en-US'));
  }

  // داده‌های اولیه و حافظه محلی سبد خرید
  let cart = [];
  try {
    const saved = localStorage.getItem('honarkadeh_cart_items');
    if (saved) {
      cart = JSON.parse(saved);
    } else {
      cart = [
        {
          id: 'prod-init-1',
          title: 'گلدان سرامیکی فیروزه‌ای با اسلیمی زرنگار',
          subtitle: 'تک‌نسخه • کارگاه کهن',
          price: 1450000,
          image: '/static/images/products/product-1.jpg',
          qty: 1
        }
      ];
    }
  } catch (e) {
    cart = [
      {
        id: 'prod-init-1',
        title: 'گلدان سرامیکی فیروزه‌ای با اسلیمی زرنگار',
        subtitle: 'تک‌نسخه • کارگاه کهن',
        price: 1450000,
        image: '/static/images/products/product-1.jpg',
        qty: 1
      }
    ];
  }

  function saveCart() {
    try {
      localStorage.setItem('honarkadeh_cart_items', JSON.stringify(cart));
    } catch (e) {
      console.warn('Could not save to localStorage', e);
    }
  }

  function openCartDropdown() {
    if (cartDropdown) {
      if (typeof notifDropdown !== 'undefined' && notifDropdown) {
        notifDropdown.classList.add('hidden');
      }
      cartDropdown.classList.remove('hidden');
      cartDropdown.classList.add('animate-fadeIn');
    }
  }

  function closeCartDropdown() {
    if (cartDropdown) {
      cartDropdown.classList.add('hidden');
    }
  }

  function toggleCartDropdown(e) {
    if (e) e.stopPropagation();
    if (cartDropdown) {
      if (cartDropdown.classList.contains('hidden')) {
        openCartDropdown();
      } else {
        closeCartDropdown();
      }
    }
  }

  // رندر کردن زنده آیتم‌ها در دراپ‌داون سبد
  function renderCartDropdown() {
    const totalQty = cart.reduce((sum, item) => sum + (item.qty || 1), 0);
    const totalPrice = cart.reduce((sum, item) => sum + ((item.price || 0) * (item.qty || 1)), 0);

    // به‌روزرسانی نشان عددی روی آیکون سبد
    if (cartBadge) {
      cartBadge.textContent = toFarsiDigits(totalQty);
      if (totalQty === 0) {
        cartBadge.classList.add('hidden');
      } else {
        cartBadge.classList.remove('hidden');
      }
    }

    // به‌روزرسانی برچسب تعداد درون منوی دراپ‌داون
    if (cartDropdownBadge) {
      cartDropdownBadge.textContent = totalQty > 0 ? `${toFarsiDigits(totalQty)} اثر هنری` : 'سبد خالی';
    }

    // به‌روزرسانی مبلغ کل
    if (totalPriceEl) {
      totalPriceEl.textContent = `${formatPrice(totalPrice)} تومان`;
    }

    // رندر آیتم‌ها در ظرف سبد
    if (cartItemsContainer) {
      if (cart.length === 0) {
        cartItemsContainer.innerHTML = `
          <div class="py-8 px-4 text-center">
            <div class="w-12 h-12 mx-auto rounded-2xl bg-[#FAF7F2] text-[#98A19C] flex items-center justify-center mb-2.5 border border-[#E8E3D9]">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
            </div>
            <p class="text-xs font-bold text-[#1E3329]">سبد خرید شما در حال حاضر خالی است</p>
            <span class="text-[11px] text-[#6B726E] mt-1 block font-light">روی + آثار هنری کلیک کنید تا به سبد افزوده شوند</span>
          </div>
        `;
      } else {
        cartItemsContainer.innerHTML = cart.map(item => {
          const imgSrc = (item.image && item.image.startsWith('.')) ? item.image.replace(/^\./, '') : (item.image || '/static/images/products/product-1.jpg');
          return `
          <div class="flex items-center gap-3 p-2.5 rounded-2xl bg-[#FAF7F2] border border-[#E8E3D9]/70 relative group transition-all duration-200 hover:border-[#2C4A3E]/40 hover:bg-[#F5F1E9]" data-id="${item.id}">
            <img src="${imgSrc}" alt="${item.title}" class="w-14 h-14 rounded-xl object-cover bg-white shrink-0 border border-[#E8E3D9] shadow-sm">
            <div class="flex-grow min-w-0">
              <h5 class="text-xs font-bold text-[#1E3329] truncate" title="${item.title}">${item.title}</h5>
              <span class="text-[10px] text-[#82533D] block truncate mt-0.5">${item.subtitle}</span>
              <div class="flex items-center justify-between mt-1.5">
                <span class="text-xs font-black text-[#2C4A3E]">${formatPrice(item.price)} تومان</span>
                <span class="text-[10px] text-[#6B726E] bg-white px-2 py-0.5 rounded-md border border-[#E8E3D9] font-medium">${toFarsiDigits(item.qty || 1)} عدد</span>
              </div>
            </div>
            <button type="button" class="remove-cart-item-btn text-[#98A19C] hover:text-red-500 p-1.5 rounded-lg hover:bg-white transition-colors shrink-0" data-id="${item.id}" title="حذف اثر از سبد">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.9" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
            </button>
          </div>
        `;
        }).join('');

        // افزودن رویداد حذف برای هر دکمه سطل زباله
        cartItemsContainer.querySelectorAll('.remove-cart-item-btn').forEach(delBtn => {
          delBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const id = delBtn.getAttribute('data-id');
            cart = cart.filter(it => it.id !== id);
            saveCart();
            renderCartDropdown();
          });
        });
      }
    }
  }

  // رندر کردن زنده صفحه سبد خرید (/cart/)
  function renderCartPage() {
    const cartPageItems = document.getElementById('cart-page-items');
    if (!cartPageItems) return;

    const totalQty = cart.reduce((sum, item) => sum + (item.qty || 1), 0);
    const subtotal = cart.reduce((sum, item) => sum + ((item.price || 0) * (item.qty || 1)), 0);
    const discount = subtotal > 0 ? Math.round(subtotal * 0.15) : 0;
    const finalTotal = subtotal - discount;

    if (cart.length === 0) {
      cartPageItems.innerHTML = `
        <div class="bg-white rounded-3xl p-12 border border-[#E8E3D9] text-center space-y-4 shadow-sm">
          <div class="w-16 h-16 mx-auto rounded-3xl bg-[#FAF7F2] text-[#98A19C] flex items-center justify-center border border-[#E8E3D9]">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
          </div>
          <h3 class="text-base font-bold text-[#1E3329]">سبد خرید شما در حال حاضر خالی است</h3>
          <p class="text-xs text-[#6B726E]">شما می‌توانید از گالری و غرفه‌های هنری دیدن کرده و اثر مورد علاقه خود را انتخاب کنید.</p>
          <a href="/shop/" class="inline-block mt-2 px-6 py-3 rounded-2xl bg-[#2C4A3E] text-white text-xs font-bold hover:bg-[#1E3329] transition-all shadow-md">
            مشاهده گالری آثار هنری
          </a>
        </div>
      `;
    } else {
      cartPageItems.innerHTML = cart.map(item => {
        const imgSrc = (item.image && item.image.startsWith('.')) ? item.image.replace(/^\./, '') : (item.image || '/static/images/products/product-1.jpg');
        return `
        <div class="bg-white rounded-3xl p-4 sm:p-6 border border-[#E8E3D9] shadow-sm flex flex-row items-center gap-3.5 sm:gap-5 relative group" data-id="${item.id}">
          <img src="${imgSrc}" alt="${item.title}" class="w-20 h-20 sm:w-28 sm:h-28 rounded-2xl object-cover bg-[#FAF7F2] shrink-0 border border-[#E8E3D9]">
          <div class="flex-grow space-y-1.5 sm:space-y-2 w-full text-right">
            <div class="flex items-center justify-between gap-2">
              <span class="text-[9px] sm:text-[10px] bg-[#E8EFEA] text-[#2C4A3E] px-2 sm:px-2.5 py-0.5 rounded-full font-bold">${item.subtitle || 'تک‌نسخه گالری'}</span>
              <button type="button" class="page-remove-cart-item text-[#98A19C] hover:text-red-500 transition-colors p-1" data-id="${item.id}" title="حذف از سبد">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
              </button>
            </div>
            <h3 class="text-xs sm:text-base font-bold text-[#1E3329] line-clamp-1 sm:line-clamp-none">${item.title}</h3>
            <div class="flex items-center justify-between pt-1 sm:pt-2 border-t border-[#E8E3D9]/60">
              <div class="flex items-center gap-1.5 sm:gap-2 border border-[#E8E3D9] rounded-xl px-1.5 sm:px-2 py-0.5 sm:py-1 bg-[#FAF7F2]">
                <button type="button" class="page-inc-cart-item w-5 h-5 sm:w-6 sm:h-6 flex items-center justify-center text-[#1E3329] font-bold hover:bg-white rounded-lg transition-colors text-xs" data-id="${item.id}">+</button>
                <span class="text-xs font-bold w-4 sm:w-5 text-center">${toFarsiDigits(item.qty || 1)}</span>
                <button type="button" class="page-dec-cart-item w-5 h-5 sm:w-6 sm:h-6 flex items-center justify-center text-[#98A19C] hover:bg-white rounded-lg transition-colors text-xs" data-id="${item.id}">-</button>
              </div>
              <div class="text-left">
                <span class="text-[10px] text-[#98A19C] block">قیمت:</span>
                <span class="text-xs sm:text-base font-extrabold text-[#1E3329]">${formatPrice((item.price || 0) * (item.qty || 1))} تومان</span>
              </div>
            </div>
          </div>
        </div>
      `;
      }).join('');

      cartPageItems.querySelectorAll('.page-inc-cart-item').forEach(btn => {
        btn.addEventListener('click', () => {
          const id = btn.getAttribute('data-id');
          const it = cart.find(x => x.id === id);
          if (it) {
            it.qty = (it.qty || 1) + 1;
            saveCart();
            renderCartDropdown();
            renderCartPage();
          }
        });
      });

      cartPageItems.querySelectorAll('.page-dec-cart-item').forEach(btn => {
        btn.addEventListener('click', () => {
          const id = btn.getAttribute('data-id');
          const it = cart.find(x => x.id === id);
          if (it) {
            if ((it.qty || 1) > 1) {
              it.qty -= 1;
            } else {
              cart = cart.filter(x => x.id !== id);
            }
            saveCart();
            renderCartDropdown();
            renderCartPage();
          }
        });
      });

      cartPageItems.querySelectorAll('.page-remove-cart-item').forEach(btn => {
        btn.addEventListener('click', () => {
          const id = btn.getAttribute('data-id');
          cart = cart.filter(x => x.id !== id);
          saveCart();
          renderCartDropdown();
          renderCartPage();
        });
      });
    }

    const summaryCountEl = document.getElementById('cart-summary-count');
    const summarySubtotalEl = document.getElementById('cart-summary-subtotal');
    const summaryDiscountEl = document.getElementById('cart-summary-discount');
    const summaryTotalEl = document.getElementById('cart-summary-total');

    if (summaryCountEl) summaryCountEl.textContent = `جمع قیمت آثار (${toFarsiDigits(totalQty)} اثر):`;
    if (summarySubtotalEl) summarySubtotalEl.textContent = `${formatPrice(subtotal)} تومان`;
    if (summaryDiscountEl) summaryDiscountEl.textContent = `${formatPrice(discount)}- تومان`;
    if (summaryTotalEl) summaryTotalEl.textContent = `${formatPrice(finalTotal)} تومان`;
  }

  // اضافه کردن اثر به سبد با کلیک روی + محصول
  function handleAddToCart(btn) {
    const card = btn.closest('article') || btn.closest('.product-card') || btn.closest('.grid > div') || btn.closest('main') || document;

    // استخراج عنوان اثر
    const titleEl = card.querySelector('h3, h1, .product-title');
    const title = titleEl ? titleEl.textContent.trim() : 'اثر هنری دست‌ساز';

    // استخراج عکس اثر (پشتیبانی از کارت‌های لیست و صفحه اختصاصی محصول)
    const imgEl = card.querySelector('img') || document.getElementById('main-product-image');
    let img = imgEl ? (imgEl.getAttribute('src') || '/static/images/products/product-1.jpg') : '/static/images/products/product-1.jpg';
    if (!img.startsWith('.') && !img.startsWith('/') && !img.startsWith('http')) {
      img = '/' + img;
    }

    // استخراج هنرمند، غرفه یا مشخصه انتخابی
    const subEl = card.querySelector('.text-\\[11px\\] span, .text-xs span, strong, .product-subtitle');
    let subtitle = subEl ? subEl.textContent.replace('کارگاه:', '').replace('هنرمند:', '').replace('غرفه:', '').trim() : 'تک‌نسخه گالری';
    const variantEl = document.getElementById('selected-variant-label');
    if (variantEl) {
      const vText = variantEl.textContent.trim();
      if (vText && !subtitle.includes(vText)) {
        subtitle += ` • مشخصه: ${vText}`;
      }
    }

    // استخراج دقیق قیمت اثر
    let price = 0;
    const priceEl = card.querySelector('.font-extrabold, [class*="font-extrabold"], .product-price, .text-2xl.font-black, .text-xl.font-black');
    if (priceEl) {
      price = parseFarsiDigits(priceEl.textContent);
    }
    if (!price) {
      const candidates = card.querySelectorAll('span, p, div');
      for (const el of candidates) {
        if (el.textContent.includes('تومان')) {
          const val = parseFarsiDigits(el.textContent);
          if (val > 10000) {
            price = val;
            break;
          }
        }
      }
    }
    if (!price) price = 1450000;

    // بررسی وجود قبلی اثر در سبد
    const existing = cart.find(item => item.title === title);
    if (existing) {
      existing.qty = (existing.qty || 1) + 1;
    } else {
      cart.unshift({
        id: 'prod-' + Date.now(),
        title: title,
        subtitle: subtitle || 'تک‌نسخه گالری',
        price: price,
        image: img,
        qty: 1
      });
    }

    saveCart();
    renderCartDropdown();
    renderCartPage();

    // فیدبک بصری روی دکمه + (سبز شدن موقت و تیک)
    const originalContent = btn.innerHTML;
    btn.classList.add('!bg-emerald-600', '!text-white', 'scale-110');
    btn.innerHTML = `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>`;
    
    setTimeout(() => {
      btn.innerHTML = originalContent;
      btn.classList.remove('!bg-emerald-600', '!text-white', 'scale-110');
    }, 600);

    // پالس روی نشان سبد خرید
    if (cartBadge) {
      cartBadge.classList.add('scale-150');
      setTimeout(() => cartBadge.classList.remove('scale-150'), 250);
    }

    // باز شدن مستقیم دراپ‌داون سبد خرید
    openCartDropdown();
  }

  // ثبت ایونت لیسنرها برای دکمه‌های باز/بستن سبد
  if (cartBtn) {
    cartBtn.addEventListener('click', toggleCartDropdown);
  }

  if (closeCartBtn) {
    closeCartBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      closeCartDropdown();
    });
  }

  // بستن در صورت کلیک در خارج از منوی سبد خرید
  document.addEventListener('click', (e) => {
    if (cartDropdown && !cartDropdown.contains(e.target) && cartBtn && !cartBtn.contains(e.target)) {
      closeCartDropdown();
    }
  });

  // اجرای اولیه رندر سبد در بارگذاری صفحه
  renderCartDropdown();
  renderCartPage();

  // ================= 4. منوی موبایل =================
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
    });
  }

  // ================= 5. اسلایدر خودکار صفحه اصلی =================
  const sliderContainer = document.getElementById('hero-slider-container');
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.slider-dot');
  const prevBtn = document.getElementById('slider-prev');
  const nextBtn = document.getElementById('slider-next');
  let currentSlide = 0;
  let slideInterval = null;

  const sliderSpeedSec = sliderContainer ? (parseInt(sliderContainer.getAttribute('data-speed'), 10) || 7) : 7;
  const sliderStopAtEnd = sliderContainer ? (sliderContainer.getAttribute('data-stop-at-end') === 'true') : false;
  const sliderIntervalMs = Math.max(2, sliderSpeedSec) * 1000;

  function showSlide(index) {
    if (!slides.length) return;
    
    if (index >= slides.length) currentSlide = 0;
    else if (index < 0) currentSlide = slides.length - 1;
    else currentSlide = index;

    slides.forEach((slide, i) => {
      if (i === currentSlide) {
        slide.classList.remove('opacity-0', 'pointer-events-none');
        slide.classList.add('opacity-100', 'pointer-events-auto');
      } else {
        slide.classList.remove('opacity-100', 'pointer-events-auto');
        slide.classList.add('opacity-0', 'pointer-events-none');
      }
    });

    dots.forEach((dot, i) => {
      if (i === currentSlide) {
        dot.classList.remove('bg-white/50', 'w-2.5');
        dot.classList.add('bg-[#C69A52]', 'w-8');
      } else {
        dot.classList.remove('bg-[#C69A52]', 'w-8');
        dot.classList.add('bg-white/50', 'w-2.5');
      }
    });
  }

  function nextSlide() {
    if (sliderStopAtEnd && currentSlide === slides.length - 1) {
      stopAutoPlay();
      return;
    }
    showSlide(currentSlide + 1);
  }

  function prevSlide() {
    showSlide(currentSlide - 1);
  }

  function startAutoPlay() {
    stopAutoPlay();
    if (sliderStopAtEnd && currentSlide === slides.length - 1) return;
    slideInterval = setInterval(nextSlide, sliderIntervalMs);
  }

  function stopAutoPlay() {
    if (slideInterval) clearInterval(slideInterval);
  }

  if (slides.length > 0) {
    showSlide(0);
    startAutoPlay();

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        nextSlide();
        startAutoPlay();
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        prevSlide();
        startAutoPlay();
      });
    }

    dots.forEach((dot, idx) => {
      dot.addEventListener('click', () => {
        showSlide(idx);
        startAutoPlay();
      });
    });

    if (sliderContainer) {
      sliderContainer.addEventListener('mouseenter', stopAutoPlay);
      sliderContainer.addEventListener('mouseleave', startAutoPlay);
    }
  }

  // ================= 6. افزودن به سبد خرید برای تمام دکمه‌های + و خرید =================
  const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
  addToCartButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      handleAddToCart(btn);
    });
  });

  // ================= 7. انتقال به صفحه محصول با کلیک روی کل کارت محصول =================
  document.addEventListener('click', (e) => {
    // صرف‌نظر کردن در صورت کلیک روی دکمه افزودن به سبد خرید، دکمه‌های فیلتر، فرم‌ها یا سطل زباله
    if (e.target.closest('.add-to-cart-btn, .remove-cart-item-btn, .category-tab-btn, .artist-filter-btn, .sort-btn, #cart-dropdown-menu, #close-banner-btn, button, input, select, textarea')) {
      return;
    }

    // شناسایی کارت محصول
    const card = e.target.closest('article, .product-card');
    if (!card) return;

    // استخراج لینک صفحه محصول از داخل کارت
    const productLink = card.querySelector('a[href*="product-detail"], h3 a, a');
    const destination = (productLink && productLink.getAttribute('href')) ? productLink.getAttribute('href') : './product-detail.html';

    // هدایت به صفحه محصول در صورتی که مقصد معتبر باشد
    if (destination && destination !== '#' && !destination.startsWith('javascript:')) {
      window.location.href = destination;
    }
  });

  // ================= 8. تب‌های انتخاب دسته‌بندی هنری (ویترین صفحه اصلی) =================
  const categoryTabBtns = document.querySelectorAll('.category-tab-btn');
  const showcaseCards = document.querySelectorAll('#products-grid article, #handicrafts-section article');

  if (categoryTabBtns.length > 0) {
    categoryTabBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();

        // به‌روزرسانی استایل ظاهری دکمه‌های تب
        categoryTabBtns.forEach(b => {
          b.classList.remove('bg-[#2C4A3E]', 'text-white', 'font-bold', 'shadow-sm');
          b.classList.add('bg-white', 'text-[#6B726E]', 'border', 'border-[#E8E3D9]', 'font-medium');
        });

        btn.classList.remove('bg-white', 'text-[#6B726E]', 'border', 'border-[#E8E3D9]', 'font-medium');
        btn.classList.add('bg-[#2C4A3E]', 'text-white', 'font-bold', 'shadow-sm');

        const selectedFilter = btn.getAttribute('data-category');

        showcaseCards.forEach(card => {
          const cardCategories = (card.getAttribute('data-category') || '').split(' ');
          if (selectedFilter === 'all' || cardCategories.includes(selectedFilter)) {
            card.style.display = '';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  // ================= 9. تب‌ها و فیلترهای سریع فروشگاه (shop.html) =================
  const shopPills = document.querySelectorAll('.shop-filter-pill');
  const shopGrid = document.querySelector('#shop-products-grid, .lg\\:col-span-3 .grid');
  const shopCards = shopGrid ? shopGrid.querySelectorAll('article') : [];

  if (shopPills.length > 0 && shopCards.length > 0) {
    shopPills.forEach(pill => {
      pill.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();

        shopPills.forEach(p => {
          p.classList.remove('bg-[#2C4A3E]', 'text-white', 'shadow-sm');
          p.classList.add('bg-white', 'border', 'border-[#E8E3D9]', 'text-[#6B726E]');
        });

        pill.classList.remove('bg-white', 'border', 'border-[#E8E3D9]', 'text-[#6B726E]');
        pill.classList.add('bg-[#2C4A3E]', 'text-white', 'shadow-sm');

        const cat = pill.getAttribute('data-category');
        shopCards.forEach(card => {
          const cardCats = (card.getAttribute('data-category') || '').split(' ');
          if (cat === 'all' || cardCats.includes(cat)) {
            card.style.display = 'flex';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  // ================= 10. وضعیت احراز هویت کاربر در هدر و آیکون پروفایل =================
  function initHeaderAuth() {
    let user = null;
    try {
      const stored = localStorage.getItem('honarkadeh_user');
      if (stored) user = JSON.parse(stored);
    } catch (e) {
      console.warn('Error reading user state', e);
    }

    const guestBtn = document.getElementById('nav-guest-btn');
    const profileWrapper = document.getElementById('nav-user-profile');
    const profileToggleBtn = document.getElementById('nav-profile-toggle-btn');
    const profileDropdown = document.getElementById('nav-profile-dropdown');

    const isServerAuth = profileWrapper && profileWrapper.getAttribute('data-authenticated') === 'true';

    if (guestBtn && profileWrapper) {
      if (isServerAuth || (user && user.isLoggedIn)) {
        document.documentElement.classList.add('user-logged-in');
        guestBtn.classList.remove('inline-flex', 'flex');
        guestBtn.classList.add('hidden');
        guestBtn.style.setProperty('display', 'none', 'important');

        profileWrapper.classList.remove('hidden');
        profileWrapper.style.setProperty('display', 'block', 'important');

        // مخفی‌سازی هر لینک ورود ثانویه در هدر
        document.querySelectorAll('header a[href*="login.html"]').forEach(link => {
          link.classList.remove('inline-flex', 'flex');
          link.classList.add('hidden');
          link.style.setProperty('display', 'none', 'important');
        });

        const serverName = document.getElementById('nav-profile-name')?.textContent?.trim();
        const userName = (user && user.name) ? user.name : (serverName && serverName !== 'کاربر گرامی' ? serverName : 'کاربر گرامی');
        const userRole = (user && user.role) ? user.role : 'buyer';
        const initial = (userName || 'هـ').trim().charAt(0);
        const isArtist = userRole === 'artist' || userRole === 'seller';

        // نام کاربر در هدر و دراپ‌داون
        const nameEls = document.querySelectorAll('#nav-profile-name, #nav-dropdown-name');
        nameEls.forEach(el => el.textContent = userName);

        // آواتارها با تم زیتونی برای خریدار و سفالی برای هنرمند
        const avatarEls = document.querySelectorAll('#nav-avatar-initial, #nav-dropdown-avatar');
        avatarEls.forEach(el => {
          el.textContent = initial;
          if (isArtist) {
            el.classList.remove('bg-[#2C4A3E]');
            el.classList.add('bg-[#82533D]');
          } else {
            el.classList.remove('bg-[#82533D]');
            el.classList.add('bg-[#2C4A3E]');
          }
        });

        // نقش در دکمه
        const roleEl = document.getElementById('nav-profile-role');
        if (roleEl) {
          roleEl.textContent = isArtist ? 'هنرمند و آفریننده' : 'خریدار هنر';
          roleEl.className = isArtist ? 'text-[9px] font-semibold text-[#82533D]' : 'text-[9px] font-semibold text-[#2C4A3E]';
        }

        // نشان نقش در دراپ‌داون
        const badgeEl = document.getElementById('nav-dropdown-role-badge');
        if (badgeEl) {
          badgeEl.textContent = isArtist ? 'هنرمند رسمی گالری' : 'خریدار و مجموعه‌دار هنر';
          badgeEl.className = isArtist 
            ? 'text-[9px] font-bold text-[#82533D] bg-[#F7EFEA] px-2 py-0.5 rounded-full mt-1 w-fit'
            : 'text-[9px] font-bold text-[#2C4A3E] bg-[#E8EFEA] px-2 py-0.5 rounded-full mt-1 w-fit';
        }

        const phoneEl = document.getElementById('nav-dropdown-phone');
        if (phoneEl && user && user.phone) phoneEl.textContent = user.phone;

        const ordersLabel = document.getElementById('nav-menu-orders-label');
        if (ordersLabel) ordersLabel.textContent = isArtist ? 'سفارش‌ها و آثار گالری' : 'سفارش‌ها و شناسنامه‌ها';

        const artistGalleryLink = document.getElementById('nav-artist-gallery-link');
        if (artistGalleryLink) {
          if (isArtist) {
            artistGalleryLink.classList.remove('hidden');
          } else {
            artistGalleryLink.classList.add('hidden');
          }
        }

      } else {
        document.documentElement.classList.remove('user-logged-in');
        guestBtn.classList.remove('hidden');
        guestBtn.classList.add('inline-flex');
        guestBtn.style.removeProperty('display');
        profileWrapper.classList.add('hidden');
        profileWrapper.style.setProperty('display', 'none', 'important');
      }
    } else {
      // پشتیبانی سراسری برای سایر صفحات: اگر کانتینر اختصاصی نبود، لینک‌های ورود در هدر به پروفایل تبدیل شوند
      const headerLoginLinks = document.querySelectorAll('header a[href*="login.html"]');
      headerLoginLinks.forEach(link => {
        if (user && user.isLoggedIn) {
          link.href = '/profile/';
          const isArtist = user.role === 'artist';
          const initial = (user.name || 'هـ').trim().charAt(0);
          link.className = 'inline-flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-bold text-[#1E3329] border border-[#E8E3D9] hover:border-[#2C4A3E] hover:bg-[#FAF7F2] transition-all shadow-xs';
          link.innerHTML = `
            <div class="relative flex items-center">
              <span class="w-6 h-6 rounded-lg ${isArtist ? 'bg-[#82533D]' : 'bg-[#2C4A3E]'} text-white flex items-center justify-center font-bold text-[11px] shadow-xs">
                ${initial}
              </span>
              <span class="absolute -bottom-0.5 -left-0.5 w-2 h-2 rounded-full bg-emerald-500 ring-1 ring-white"></span>
            </div>
            <span class="text-xs font-bold">${user.name || 'پروفایل من'}</span>
          `;
          link.title = 'ورود به پروفایل کاربری';
        }
      });
    }

    // باز و بسته شدن دراپ‌داون پروفایل با انیمیشن و کلیک مستقیم
    if (profileToggleBtn && profileDropdown) {
      profileToggleBtn.onclick = function(e) {
        e.stopPropagation();
        const notifMenu = document.getElementById('notif-dropdown');
        const cartMenu = document.getElementById('cart-dropdown-menu') || document.getElementById('cart-dropdown');
        if (notifMenu) notifMenu.classList.add('hidden');
        if (cartMenu) cartMenu.classList.add('hidden');
        profileDropdown.classList.toggle('hidden');
      };

      document.addEventListener('click', (e) => {
        if (!profileDropdown.contains(e.target) && !profileToggleBtn.contains(e.target)) {
          profileDropdown.classList.add('hidden');
        }
      });
    }
  }

  // اجرای اولیه احراز هویت هدر
  initHeaderAuth();
});

// تابع سراسری خروج از حساب کاربری
window.logoutHonarkadeh = function() {
  try {
    localStorage.removeItem('honarkadeh_user');
    document.documentElement.classList.remove('user-logged-in');
  } catch (e) {}
  window.location.href = '/logout/';
};


