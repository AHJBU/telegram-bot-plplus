
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from PIL import Image, ImageDraw, ImageFont

TOKEN = "7666664099:AAHRukdO-aNygOR6UlMO2DbbqKQvTeYLo0Y"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي نصًا، وسأحوّله إلى صورة داخل القالب!")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # تحميل القالب
    img = Image.open("template.png")
    draw = ImageDraw.Draw(img)

    # إعداد الخط
    font = ImageFont.truetype("Cairo-Bold.ttf", 45)

    # حساب موقع النص في منتصف الصورة
    image_width, image_height = img.size
    text_width, text_height = draw.textsize(user_text, font=font)
    x = (image_width - text_width) / 2
    y = (image_height - text_height) / 2

    # رسم النص على الصورة
    draw.text((x, y), user_text, fill="black", font=font)

    # حفظ الصورة المؤقتة
    output_path = "output.png"
    img.save(output_path)

    # إرسال الصورة كرد
    await update.message.reply_photo(photo=open(output_path, 'rb'))

# إعداد البوت
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

print("Bot is running...")
app.run_polling()
