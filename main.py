from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from PIL import Image, ImageDraw, ImageFont
import textwrap

# ✅ التوكن الخاص بك
TOKEN = "7666664099:AAHRukdO-aNygOR6UlMO2DbbqKQvTeYLo0Y"

# ✅ إعدادات منطقة النص داخل القالب
TEXT_AREA = {
    "x": 100,          # بداية المربع على المحور X
    "y": 300,          # بداية المربع على المحور Y
    "width": 800,      # عرض منطقة النص
    "height": 200      # ارتفاع منطقة النص
}

FONT_PATH = "Cairo-Bold.ttf"  # تأكد من وجود الملف في نفس المجلد
DEFAULT_FONT_SIZE = 36        # تغيير الاسم لتجنب التعارض
TEXT_COLOR = (60, 60, 60)    # لون النص (رمادي غامق)
BACKGROUND_COLOR = (255, 255, 255)  # لون خلفية النص (أبيض)

# ✅ دالة تقسيم النص إلى أسطر تناسب عرض معين (محسنة)
def wrap_text(text, font, max_width, max_lines=None):
    # حساب متوسط عدد الحروف في السطر بناءً على حجم الخط والعرض
    avg_char_width = font.getlength("ا")  # استخدام حرف عربي كمرجع
    max_chars = int(max_width / avg_char_width) * 0.8  # عامل أمان 0.8
    
    wrapper = textwrap.TextWrapper(
        width=max_chars,
        break_long_words=True,
        replace_whitespace=False
    )
    
    lines = wrapper.wrap(text)
    
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1] + "..."  # إضافة نقاط إذا تم قطع النص
    
    return lines

# ✅ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي نصًا وسأحوله إلى صورة مع التصميم المطلوب")

# ✅ عند استلام رسالة نصية
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        # فتح صورة القالب
        img = Image.open("template.png")
        draw = ImageDraw.Draw(img)
        
        # استخدام متغير محلي لحجم الخط بدلاً من العام
        current_font_size = DEFAULT_FONT_SIZE
        
        # تحميل الخط مع حجم أكبر أولاً لتحسين الدقة
        font = ImageFont.truetype(FONT_PATH, current_font_size * 2)
        
        # تقسيم النص مع مراعاة عرض المربع
        lines = wrap_text(user_text, font, TEXT_AREA["width"])
        
        # حساب ارتفاع السطر
        test_bbox = font.getbbox("ص")  # استخدام حرف عربي طويل للقياس
        line_height = test_bbox[3] - test_bbox[1]
        line_height = int(line_height * 0.8)  # تعديل الارتفاع
        
        # حساب الارتفاع الكلي للنص
        total_text_height = len(lines) * line_height
        
        # إذا كان النص أطول من ارتفاع المربع، نضبط حجم الخط
        while total_text_height > TEXT_AREA["height"] and current_font_size > 10:
            current_font_size -= 2
            font = ImageFont.truetype(FONT_PATH, current_font_size * 2)
            lines = wrap_text(user_text, font, TEXT_AREA["width"])
            test_bbox = font.getbbox("ص")
            line_height = test_bbox[3] - test_bbox[1]
            line_height = int(line_height * 0.8)
            total_text_height = len(lines) * line_height
        
        # التوسيط العمودي داخل المنطقة
        y_start = TEXT_AREA["y"] + (TEXT_AREA["height"] - total_text_height) / 2
        
        # رسم كل سطر من النص
        for line in lines:
            # حساب عرض النص للتوسيط الأفقي
            text_width = font.getlength(line)
            x = TEXT_AREA["x"] + (TEXT_AREA["width"] - text_width) / 2
            
            # رسم النص مع حواف أكثر وضوحاً
            draw.text(
                (x, y_start),
                line,
                fill=TEXT_COLOR,
                font=font,
                language='ar'
            )
            
            y_start += line_height
        
        # حفظ الصورة الناتجة
        output_path = "output.png"
        img.save(output_path)
        
        # إرسال الصورة للمستخدم
        await update.message.reply_photo(photo=open(output_path, 'rb'))
        
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {str(e)}")

# ✅ تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot is running...")
    app.run_polling()
