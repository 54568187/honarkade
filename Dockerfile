FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# نصب پیش‌نیازهای سیستمی برای pillow و تصاویر
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# اجرای میگریشن‌ها، جمع‌آوری فایل‌های استاتیک و مقداردهی داده‌های اولیه
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput
RUN python manage.py seed_data

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
