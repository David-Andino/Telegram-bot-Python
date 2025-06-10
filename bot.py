from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp
import os
import uuid


TELEGRAM_TOKEN = 'Aquí va el token de tu bot'

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hola, envíame un enlace de YouTube y dime si lo quieres en MP3 o MP4.")

# Manejo de mensajes con enlaces
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "youtube.com" in text or "youtu.be" in text:
        await update.message.reply_text("🔍 ¿Quieres MP3 o MP4? Escribe /mp3 o /mp4 seguido del enlace.")
    else:
        await update.message.reply_text("❌ Eso no parece un enlace de YouTube válido.")

# Descarga de MP3
async def download_mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("📎 Debes escribir el comando así: /mp3 <enlace>")
        return

    url = context.args[0]
    filename = f"{uuid.uuid4()}.mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(uploader)s - %(title)s.%(ext)s',
        'ffmpeg_location': 'D:/Descargas/ffmpeg-7.1.1-essentials_build/ffmpeg-7.1.1-essentials_build/bin',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    await update.message.reply_text("🎧 Descargando MP3...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            await update.message.reply_audio(audio=open(filename, 'rb'))
        finally:
            if os.path.exists(filename):
                os.remove(filename)

# Descarga de MP4
async def download_mp4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("📎 Debes escribir el comando así: /mp4 <enlace>")
        return

    url = context.args[0]
    filename = f"{uuid.uuid4()}.mp4"
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(uploader)s - %(title)s.%(ext)s',
        'ffmpeg_location': 'D:/Descargas/ffmpeg-7.1.1-essentials_build/ffmpeg-7.1.1-essentials_build/bin',
        'merge_output_format': 'mp4',
    }

    await update.message.reply_text("📹 Descargando MP4...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            await update.message.reply_video(video=open(filename, 'rb'))
        finally:
            if os.path.exists(filename):
                os.remove(filename)

# Configurar bot
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("mp3", download_mp3))
app.add_handler(CommandHandler("mp4", download_mp4))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == '__main__':
    print("🤖 Bot en marcha...")
    app.run_polling()
