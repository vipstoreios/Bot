import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from mega import Mega
from flask import Flask
from threading import Thread

# زانیارییە نوێیەکانت
API_TOKEN = '8400153721:AAHIiqTEQzVAB8OfuENdPyAGx7IDCrPWpfQ'
MEGA_EMAIL = 'kakaado.tech@gmail.com'
MEGA_PASSWORD = 'Ostaz.kim88'

app = Flask('')
@app.route('/')
def home(): return "Fly Store Bot is Active with New Token!"

def run_web(): app.run(host='0.0.0.0', port=8080)

def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    update.message.reply_text(f"سڵاوێکی زۆر گەرم، {user_name} گیان! ❤️ بەخێربێیت بۆ بۆتی فڵای ستۆر.\n\nبۆتەکە بە بەرزترین خێرایی کار دەکات ✅\nفایلی IPA بنێرە یان فۆرواردی بکە لێرە.")

def handle_docs(update: Update, context: CallbackContext):
    msg = update.message.reply_text("🚀 دەستم پێ کرد... تکایە کەمێک چاوەڕێبە.")
    file_doc = update.message.document
    file_name = file_doc.file_name
    
    try:
        # ١. قۆناغی داگرتن
        msg.edit_text(f"📥 خەریکی داگرتنی فایلەکەم...\n📦 {file_name}")
        file_path = context.bot.get_file(file_doc.file_id).download()
        
        # ٢. قۆناغی بەرزکردنەوە بۆ Mega
        msg.edit_text("📤 خەریکی بەرزکردنەوەم بۆ Mega... (بە سەریعی 🚀)")
        mega = Mega().login(MEGA_EMAIL, MEGA_PASSWORD)
        uploaded_file = mega.upload(file_path)
        link = mega.get_upload_link(uploaded_file)
        
        # ٣. ناردنی لینکەکە
        msg.edit_text(f"✅ فەرموو کارەکەت تەواو بوو:\n\n📦 ناو: {file_name}\n🔗 لینک: {link}")
        
        if os.path.exists(file_path): os.remove(file_path)
    except Exception as e:
        msg.edit_text(f"❌ ببورە کێشەیەک دروست بوو: {str(e)}")

def handle_text(update: Update, context: CallbackContext):
    update.message.reply_text("بۆتەکە بە سەریعی کار دەکات! ✅ تەنها فایلی IPA بنێرە.")

def main():
    Thread(target=run_web).start()
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, handle_docs))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
