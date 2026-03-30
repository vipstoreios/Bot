import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from mega import Mega
from flask import Flask
from threading import Thread

# زانیارییەکانت
API_TOKEN = '8400153721:AAHIiqTEQzVAB8OfuENdPyAGx7IDCrPWpfQ'
MEGA_EMAIL = 'kakaado.tech@gmail.com'
MEGA_PASSWORD = 'Ostaz.kim88'

# ڕێکخستنی Flask بۆ ئەوەی سێرڤەرەکە نەکەوێت
app = Flask('')
@app.route('/')
def home(): return "Fly Store Bot is Online!"

def run_web(): app.run(host='0.0.0.0', port=8080)

# دروستکردنی شریتی پێشکەوتن
def progress_bar(current, total):
    if total == 0: return "0%"
    percent = current * 100 / total
    filled = int(10 * current // total)
    bar = '🔹' * filled + '▫️' * (10 - filled)
    return f"{bar} {percent:.1f}%"

def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    update.message.reply_text(f"سڵاوێکی زۆر گەرم لە تۆی خۆشەویست، {user_name} گیان! ❤️\n\nبۆتی فڵای ستۆر بەرزترین خێرایی و وەڵامدانەوەی هەیە. 🚀\nفایلی IPA بنێرە یان فۆرواردی بکە، من کارەکەت بۆ دەکەم.")

def handle_docs(update: Update, context: CallbackContext):
    # ناردنی نامەی دەستپێکردن
    status_msg = update.message.reply_text("🚀 دەستم پێکرد... خەریکی پشکنینی فایلەکەم.")
    
    file_doc = update.message.document
    file_name = file_doc.file_name
    file_id = file_doc.file_id
    
    try:
        # ١. قۆناغی داگرتن
        status_msg.edit_text(f"📥 خەریکی داگرتنم...\n📦 {file_name}")
        file_path = context.bot.get_file(file_id).download()
        
        # ٢. قۆناغی بەرزکردنەوە بۆ Mega
        status_msg.edit_text("📤 دەستی کرد بە بەرزکردنەوە بۆ Mega...")
        mega = Mega().login(MEGA_EMAIL, MEGA_PASSWORD)
        
        # لێرەدا مێگا فایلەکە بەرز دەکاتەوە
        uploaded_file = mega.upload(file_path)
        link = mega.get_upload_link(uploaded_file)
        
        # ٣. کۆتایی و ناردنی لینک
        status_msg.edit_text(f"✅ کارەکە بە سەرکەوتوویی تەواو بوو!\n\n📦 ناو: {file_name}\n🔗 لینک: {link}")
        
        # سڕینەوەی فایلەکە لە سێرڤەر بۆ ئەوەی جێگە نەگرێت
        if os.path.exists(file_path):
            os.remove(file_path)
            
    except Exception as e:
        status_msg.edit_text(f"❌ کێشەیەک دروست بوو: {str(e)}")

def handle_text(update: Update, context: CallbackContext):
    update.message.reply_text("بۆتەکە بە سەریعی کار دەکات! ✅\nتەنها فایلی IPA بنێرە بۆ ئەوەی بۆت بکەم بە لینکی مێگا.")

def main():
    # دەستپێکردنی سێرڤەری وێب لە پشتەوە
    Thread(target=run_web).start()
    
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    
    # وەرگرتنی فایل (ناردنی ئاسایی یان فۆرواردکراو)
    dp.add_handler(MessageHandler(Filters.document, handle_docs))
    
    # وەڵامدانەوەی هەر نامەیەکی تێکست
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
