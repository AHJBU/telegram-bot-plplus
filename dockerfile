FROM python:3.9-slim

# تثبيت حزم النظام المطلوبة لـ Pillow
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# نسخ الملفات مع تجنب ملفات غير ضرورية
COPY requirements.txt .
COPY main.py .
COPY Cairo-Bold.ttf .
COPY template.png .

# تثبيت المكتبات
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
