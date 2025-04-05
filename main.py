from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from PIL import Image, ImageDraw, ImageFont
import textwrap
import arabic_reshaper
from bidi.algorithm import get_display

# التوكن الخاص بك
TOKEN = "7666664099:AAHRukdO-aNygOR6UlMO2DbbqKQvTeYLo0Y"

# إعدادات منطقة النص داخل القالب
TEXT_AREA = {
    "x": 100,
    "y": 300,
    "width": 800,
    "height": 400  # تم زيادة الارتفاع ليتناسب مع محتوى الصورة
}

FONT_PATH = "Cairo-Bold.ttf"
DEFAULT_FONT_SIZE = 40
TEXT_COLOR = (60, 60, 60)
BACKGROUND_COLOR = (255, 255, 255, 0)  # شفاف

# دالة معالجة النص العربي
def prepare_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# دالة تقسيم النص مع تحسين للغة العربية
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_line_processed = prepare_arabic_text(test_line)
        width = font.getlength(test_line_processed)
        
        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

# دالة حساب حجم الخط المناسب
def calculate_font_size(text, draw_area):
    max_font = 60
    min_font = 20
    words_count = len(text.split())
    
    # حساب حجم الخط المبدئي بناء على عدد الكلمات
    if words_count < 10:
        return max_font
    elif words_count < 20:
        return 40
    elif words_count < 30:
        return 32
    else:
        return min_font

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        
        # فتح صورة القالب
        template_img = Image.open("template.png")
        img = Image.new("RGBA", template_img.size, (255, 255, 255, 0))
        img.paste(template_img, (0, 0))
        draw = ImageDraw.Draw(img)
        
        # حساب حجم الخط الأولي
        current_font_size = calculate_font_size(user_text, TEXT_AREA)
        font = ImageFont.truetype(FONT_PATH, current_font_size)
        
        # تقسيم النص إلى أسطر
        wrapped_lines = wrap_text(user_text, font, TEXT_AREA["width"])
        
        # حساب المسافات
        test_char = "ص"
        bbox = font.getbbox(test_char)
        line_height = bbox[3] - bbox[1] +
