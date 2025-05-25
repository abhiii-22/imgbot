from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from rembg import remove
from PIL import Image
from io import BytesIO

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *Abhi's Background Remover Bot!*\n\n"
        "📸 Just send me a photo, and I’ll remove the background for you.\n"
        "⏳ Please wait a few seconds after sending a photo.\n\n"
        "Made with ❤️ by Abhi",
        parse_mode="Markdown"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    processing_msg = await update.message.reply_text("🛠 Removing background... Please wait ⏳")

    try:
        photo = await update.message.photo[-1].get_file()
        file_bytes = await photo.download_as_bytearray()

        input_image = Image.open(BytesIO(file_bytes)).convert("RGBA")  # Ensure image is in proper format
        output_image = remove(input_image)

        output_bytes = BytesIO()
        output_image.save(output_bytes, format='PNG')
        output_bytes.seek(0)

        await update.message.reply_document(document=output_bytes, filename='no_bg.png')

    except Exception as e:
        await update.message.reply_text(f"❌ An error occurred: {str(e)}")

    finally:
        await processing_msg.delete()

async def handle_invalid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Please send a photo. Other file types are not supported.")

def main():
    TOKEN = "8142395334:AAGp6Qmf9bs865Xg6XBguP9zIcMhtLcUJ0A"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(~filters.PHOTO & ~filters.COMMAND, handle_invalid))  # Handle non-photo, non-command

    app.run_polling()

if __name__ == "__main__":
    main()
