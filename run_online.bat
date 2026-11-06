@echo off
chcp 65001 >nul
title هنرکده - سرور آنلاین دامنه اختصاصی (kadehonar.ir)
echo =========================================================
echo       در حال اجرای وب‌سایت هنرکده روی دامنه اختصاصی
echo                    kadehonar.ir
echo =========================================================
echo.
echo ۱. در حال اجرای سرور اصلی جنگو...
start "Django Server" /B python manage.py runserver 127.0.0.1:8000
timeout /t 3 >nul
echo.
echo ۲. در حال اتصال به دامنه ثابت kadehonar.ir...
echo.
echo =========================================================
echo   سایت شما هم‌اکنون با آدرس‌های زیر در اینترنت فعال است:
echo   1. https://kadehonar.ir
echo   2. https://trapdoor-reproduce-equation.ngrok-free.dev
echo =========================================================
echo.
.\ngrok.exe http 8000 --url https://trapdoor-reproduce-equation.ngrok-free.dev --authtoken 3Lit18VbuciK5zMVkknp2sXc8B8_3SDVZADn1KauwqFkMc5Vn
pause
