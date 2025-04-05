from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from PIL import Image, ImageDraw, ImageFont

TOKEN = "7666664099:AAHRukdO-aNygOR6UlMO2DbbqKQvTeYLo0Y"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي نصًا وسأعيد لك صورة بتصميم PL Plus")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    img = Image.open("template.png")
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("Cairo-Bold.ttf", 45)

    image_width, image_height = img.size
    bbox = draw.textbbox((0, 0), user_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (image_width - text_width) / 2
    y = (image_height - text_height) / 2

    draw.text((x, y), user_text, fill="black", font=font)

    output_path = "output.png"
    img.save(output_path)

    await update.message.reply_photo(photo=open(output_path, 'rb'))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

print("Bot is running...")
app.run_polling()
