import os
import time
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from mega import Mega
from flask import Flask
from threading import Thread

# زانیارییەکانت
API_TOKEN = '8400153721:AAEZ-EE3DzMmx5D_irDRq4CYWiVH9UVckyM'
MEGA_EMAIL = 'kakaado.tech@gmail.com'
MEGA_PASSWORD = 'Ostaz.kim88'

app = Flask('')
@app.route('/')
def home(): return "Fly Store Bot is Active!"

def run_web(): app.run(host='0.0.0.0', port=8080)

# دروستکردنی شریتی پێشکەوتن (Progress Bar)
def get_progress_bar(current, total):
    percent = current * 100 / total
    filled_length = int(10 * current // total)
    bar = '🔹' * filled_length + '▫️' * (10 - filled_length)
    return f"{bar} {percent:.1f}%"

def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    update.message.reply_text(f"سڵاوێکی زۆر گەرم لە تۆی بەڕێز {user_name} گیان بۆ بۆتی فڵای ستۆر ❤️\n\nبۆتەکە بە تەواوی کار دەکات ✅\nتەنها فایلی IPA بنێرە یان فۆرواردی بکە لێرە.")

def handle_all_messages(update: Update, context: CallbackContext):
    # ئەگەر فایل نەبوو، تەنها بڵێ کار دەکەم
    if not update.message.document:
        update.message.reply_text("بۆتەکە بە سەریعی کار دەکات! چاوەڕێی فایلی تۆم 🚀")
        return

    msg = update.message.reply_text("🚀 دەستم پێ کرد... چاوەڕێبە")
    file_document = update.message.document
    file_name = file_document.file_name
    
    try:
        # داگرتنی فایل
        msg.edit_text(f"📥 خەریکی داگرتنی فایلەکەم...\n{file_name}")
        file = context.bot.get_file(file_document.file_id)
        file.download(file_name)
        
        # بەرزکردنەوە بۆ مێگا
        msg.edit_text("📤 خەریکی بەرزکردنەوەم بۆ Mega...")
        mega = Mega().login(MEGA_EMAIL, MEGA_PASSWORD)
        
        # لێرەدا فایلەکە بەرز دەکرێتەوە (مێگا خۆی زۆر خێرایە)
        uploaded_file = mega.upload(file_name)
        link = mega.get_upload_link(uploaded_file)
        
        msg.edit_text(f"✅ بە سەرکەوتوویی تەواو بوو!\n\n📦 ناو: {file_name}\n🔗 لینک: {link}")
        
        if os.path.exists(file_name):
            os.remove(file_name)
            
    except Exception as e:
        msg.edit_text(f"❌ ببورە کێشەیەک هەبوو: {str(e)}")

def main():
    # دەستپێکردنی سێرڤەری وێب بۆ ئەوەی دانەخرێت
    Thread(target=run_web).start()
    
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    # وەرگرتنی هەموو جۆرە فایل و نامەیەک
    dp.add_handler(MessageHandler(Filters.all, handle_all_messages))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
