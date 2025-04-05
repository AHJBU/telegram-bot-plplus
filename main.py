from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from PIL import Image, ImageDraw, ImageFont

# ✅ التوكن الخاص بك
TOKEN = "7666664099:AAHRukdO-aNygOR6UlMO2DbbqKQvTeYLo0Y"

# ✅ إعدادات منطقة النص داخل القالب
TEXT_AREA = {
    "x": 100,
    "y": 300,
    "width": 800,
    "height": 200
}

FONT_PATH = "Cairo-Bold.ttf"
FONT_SIZE = 36
TEXT_COLOR = (60, 60, 60)

# ✅ دالة تقسيم النص إلى أسطر تناسب عرض معين
def wrap_text(text, draw, font, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        width = draw.textlength(test_line, font=font)
        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

# ✅ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي نصًا وسأعيد لك صورة بتصميم PL Plus")

# ✅ عند استلام رسالة نصية
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    img = Image.open("template.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    lines = wrap_text(user_text, draw, font, TEXT_AREA["width"])
    line_height = font.getbbox("Ay")[3] + 10  # ارتفاع السطر + تباعد بسيط
    total_text_height = len(lines) * line_height

    # التوسيط العمودي داخل المنطقة
    y_start = TEXT_AREA["y"] + (TEXT_AREA["height"] - total_text_height) / 2

    for line in lines:
        text_width = draw.textlength(line, font=font)
        x = TEXT_AREA["x"] + (TEXT_AREA["width"] - text_width) / 2
        draw.text((x, y_start), line, fill=TEXT_COLOR, font=font)
        y_start += line_height

    img.save("output.png")
    await update.message.reply_photo(photo=open("output.png", 'rb'))

# ✅ تشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

print("Bot is running...")
app.run_polling()
