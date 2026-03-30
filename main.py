import os
import telebot
from mega import Mega
from flask import Flask
from threading import Thread

API_TOKEN = '8400153721:AAEZ-EE3DzMmx5D_irDRq4CYWiVH9UVckyM'
MEGA_EMAIL = 'kakaado.tech@gmail.com'
MEGA_PASSWORD = 'Ostaz.kim88'

bot = telebot.TeleBot(API_TOKEN)

app = Flask('')
@app.route('/')
def home():
    return "Fly Store Bot is Live and Ready!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "بەخێربێیت بۆ بۆتی فڵای ستۆر 🚀\nفایلی IPA یان هەر فایلێکی تر بنێرە تا بۆت بکەم بە لینکی مێگا.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        msg = bot.reply_to(message, "⏳ خەریکی داگرتنی فایلەکەم لە تەلەگرام...")
        
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name
        
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        bot.edit_message_text("📤 ئێستا بەرز دەکرێتەوە بۆ MEGA...", message.chat.id, msg.message_id)
        
        # چوونە ژوورەوەی مێگا لە کاتی ناردنی فایلەکە دەکرێت بۆ ئەوەی بێ کێشە بێت
        mega = Mega()
        m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)
        file = m.upload(file_name)
        link = m.get_upload_link(file)
        
        final_text = f"✅ فایلەکە ئامادەیە\n\n📦 ناو: {file_name}\n🔗 لینک: {link}"
        bot.edit_message_text(final_text, message.chat.id, msg.message_id)
        
        if os.path.exists(file_name):
            os.remove(file_name)
            
    except Exception as e:
        bot.reply_to(message, f"❌ کێشەیەک ڕوویدا: {str(e)}")

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    bot.polling(none_stop=True)
