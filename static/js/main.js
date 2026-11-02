/**
 * Honarkadeh Main JavaScript
 * هندل کردن اسلایدر اتوماتیک، مگامنو، سبد خرید، نوتیفیکیشن و بنر تبلیغاتی
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

  // ================= 3. سبد خرید کشویی (Cart Drawer) =================
  const cartDrawerBtn = document.getElementById('cart-drawer-btn');
  const cartDrawer = document.getElementById('cart-drawer');
  const cartOverlay = document.getElementById('cart-overlay');
  const closeCartBtn = document.getElementById('close-cart-btn');

  function openCart() {
    if (cartDrawer && cartOverlay) {
      cartDrawer.classList.remove('translate-x-full');
      cartOverlay.classList.remove('hidden');
      document.body.classList.add('overflow-hidden');
    }
  }

  function closeCart() {
    if (cartDrawer && cartOverlay) {
      cartDrawer.classList.add('translate-x-full');
      cartOverlay.classList.add('hidden');
      document.body.classList.remove('overflow-hidden');
    }
  }

  if (cartDrawerBtn) cartDrawerBtn.addEventListener('click', openCart);
  if (closeCartBtn) closeCartBtn.addEventListener('click', closeCart);
  if (cartOverlay) cartOverlay.addEventListener('click', closeCart);

  // ================= 4. منوی موبایل =================
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
    });
  }

  // ================= 5. اسلایدر خودکار صفحه اصلی =================
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.slider-dot');
  const prevBtn = document.getElementById('slider-prev');
  const nextBtn = document.getElementById('slider-next');
  let currentSlide = 0;
  let slideInterval = null;

  function showSlide(index) {
    if (!slides.length) return;
    
    // تصحیح بازه اندیس
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
    showSlide(currentSlide + 1);
  }

  function prevSlide() {
    showSlide(currentSlide - 1);
  }

  function startAutoPlay() {
    stopAutoPlay();
    slideInterval = setInterval(nextSlide, 5000); // تعویض خودکار هر ۵ ثانیه
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

    // توقف در هاور و ادامه هنگام خروج ماوس
    const sliderContainer = document.getElementById('hero-slider-container');
    if (sliderContainer) {
      sliderContainer.addEventListener('mouseenter', stopAutoPlay);
      sliderContainer.addEventListener('mouseleave', startAutoPlay);
    }
  }

  // ================= 6. افزودن به سبد خرید تستی برای کارت‌ها =================
  const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
  const cartBadge = document.getElementById('cart-count-badge');
  let cartCount = 0;

  addToCartButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      cartCount++;
      if (cartBadge) {
        cartBadge.textContent = cartCount;
        cartBadge.classList.add('scale-125');
        setTimeout(() => cartBadge.classList.remove('scale-125'), 200);
      }
      openCart();
    });
  });
});
