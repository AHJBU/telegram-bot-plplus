from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from PIL import Image, ImageDraw, ImageFont

# ✅ التوكن الخاص ببوتك
TOKEN = "7666664099:AAHRukdO-aNygOR6UlMO2DbbqKQvTeYLo0Y"

# ✅ تعريف منطقة النص داخل القالب
TEXT_AREA = {
    "x": 100,
    "y": 300,
    "width": 800,
    "height": 200
}

# ✅ إعداد الخط
FONT_PATH = "Cairo-Bold.ttf"
FONT_SIZE = 36
TEXT_COLOR = (60, 60, 60)

# ✅ دالة لتقسيم النص الطويل لعدة أسطر
def wrap_text(text, draw, font, max_width):
    lines = []
    words = text.split()
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

# ✅ دالة الرد على /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي نصًا وسأعيد لك صورة بتصميم PL Plus")

# ✅ دالة التعامل مع النصوص
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    img = Image.open("template.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    lines = wrap_text(user_text, draw, font, TEXT_AREA["width"])
    total_text_height = sum([draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines])
    line_height = total_text_height / len(lines)

    # حساب البداية لتوسيط النص عموديًا
    y = TEXT_AREA["y"] + (TEXT_AREA["height"] - total_text_height) / 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = TEXT_AREA["x"] + (TEXT_AREA["width"] - text_width) / 2
        draw.text((x, y), line, fill=TEXT_COLOR, font=font)
        y += line_height

    img.save("output.png")
    await update.message.reply_photo(photo=open("output.png", 'rb'))

# ✅ إعداد البوت وتشغيله
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

print("Bot is running...")
app.run_polling()
