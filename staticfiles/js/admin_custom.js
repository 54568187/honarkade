/**
 * Honarkadeh Admin Custom JS Experience Enhancements
 * 1. کلیک‌پذیری کل ردیف جدول‌های ادمین
 * 2. میانبر کیبورد Ctrl+S / Cmd+S برای ذخیره فوری فرم‌ها بدون نیاز به اسکرول
 * 3. بهینه‌سازی نوار ذخیره شناور
 */
document.addEventListener("DOMContentLoaded", function () {
  
  // ۱. قابلیت کلیک‌پذیر بودن کل ردیف جدول‌ها
  document.addEventListener("click", function (event) {
    const target = event.target;

    // اگر کلیک روی دکمه، چک‌باکس یا لینک مستقیم بوده ناوبری دستی انجام نشود
    if (
      target.closest(
        'input, select, textarea, button, a, label, .action-checkbox, [role="button"]'
      )
    ) {
      return;
    }

    const row = target.closest("table tbody tr");
    if (!row) return;

    const editLink = row.querySelector("th a, td a");
    if (editLink && editLink.href && !editLink.href.includes("javascript:")) {
      if (event.ctrlKey || event.metaKey) {
        window.open(editLink.href, "_blank");
      } else {
        window.location.href = editLink.href;
      }
    }
  });

  // ۲. میانبر کیبورد هوشمند Ctrl + S یا Cmd + S برای ذخیره فوری فرم
  document.addEventListener("keydown", function (event) {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s") {
      const saveButton = document.querySelector(
        'form[id$="_form"] button[type="submit"][name="_save"], form[id$="_form"] input[type="submit"][name="_save"], .submit-row button[type="submit"], button[type="submit"].default'
      );
      if (saveButton) {
        event.preventDefault();
        saveButton.click();
      }
    }
  });

});
