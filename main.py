import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from mega import Mega
from flask import Flask
from threading import Thread

# ئەمانە وەک خۆی بهێڵەرەوە
API_TOKEN = '8400153721:AAEZ-EE3DzMmx5D_irDRq4CYWiVH9UVckyM'
MEGA_EMAIL = 'kakaado.tech@gmail.com'
MEGA_PASSWORD = 'Ostaz.kim88'

# ڕێکخستنی فلاک بۆ ئەوەی ڕێندەر نەیکوژێنێتەوە
app = Flask('')
@app.route('/')
def home(): return "Fly Store Bot is Running!"

def run_web(): app.run(host='0.0.0.0', port=8080)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سڵاو کاک ئادۆ! فایلی IPA بنێرە تا بۆت بکەم بە لینکی مێگا.")

def handle_docs(update: Update, context: CallbackContext):
    msg = update.message.reply_text("⏳ خەریکی داگرتنی فایلەکەم (تەنانەت ئەگەر قەبارەی گەورەش بێت)...")
    try:
        file = context.bot.get_file(update.message.document.file_id)
        file_name = update.message.document.file_name
        file.download(file_name)
        
        msg.edit_text("📤 ئێستا بەرز دەکرێتەوە بۆ مێگا...")
        mega = Mega().login(MEGA_EMAIL, MEGA_PASSWORD)
        uploaded_file = mega.upload(file_name)
        link = mega.get_upload_link(uploaded_file)
        
        msg.edit_text(f"✅ فەرموو فایلی ئامادەیە:\n\n📦 {file_name}\n🔗 {link}")
        if os.path.exists(file_name): os.remove(file_name)
    except Exception as e:
        msg.edit_text(f"❌ کێشەیەک دروست بوو: {str(e)}")

def main():
    Thread(target=run_web).start()
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, handle_docs))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
