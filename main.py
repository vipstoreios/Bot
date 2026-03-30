import os
import telebot
from mega import Mega
from flask import Flask
from threading import Thread

# --- زانیارییەکانی جەنابت ---
API_TOKEN = '8400153721:AAEZ-EE3DzMmx5D_irDRq4CYWiVH9UVckyM'
MEGA_EMAIL = 'kakaado.tech@gmail.com'
MEGA_PASSWORD = 'Ostaz.kim88'

bot = telebot.TeleBot(API_TOKEN)
mega = Mega()

# چوونە ناو ئەکاونتی مێگا
try:
    m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)
    print("✅ Login to MEGA successful!")
except Exception as e:
    print(f"❌ MEGA Login Error: {e}")

# سێرڤەر بۆ ئەوەی ڕێگری بکات لە وەستانی بۆتەکە لەسەر Render
app = Flask('')
@app.route('/')
def home():
    return "Fly Store Bot is Running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "بەخێربێیت بۆ بۆتی فڵای ستۆر 🚀\nفایلەکە بنێرە تا بۆت بکەم بە لینکی مێگا.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        msg = bot.reply_to(message, "⏳ خەریکی داگرتنی فایلەکەم لە تەلەگرام...")
        
        # وەرگرتنی زانیاری فایل
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name
        
        # پاشەکەوتکردنی کاتی لەسەر سێرڤەر
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        bot.edit_message_text("📤 ئێستا بەرز دەکرێتەوە بۆ MEGA...", message.chat.id, msg.message_id)
        
        # ناردن بۆ مێگا
        file = m.upload(file_name)
        link = m.get_upload_link(file)
        
        # ناردنەوەی وەڵامی کۆتایی
        final_text = (
            f"✅ فایلەکە ئامادەیە بۆ فڵای ستۆر\n\n"
            f"📦 ناو: {file_name}\n"
            f"🔗 لینک: {link}"
        )
        bot.edit_message_text(final_text, message.chat.id, msg.message_id)
        
        # سڕینەوەی فایلەکە لە سێرڤەر بۆ ئەوەی جێگا نەگرێت
        if os.path.exists(file_name):
            os.remove(file_name)
            
    except Exception as e:
        bot.reply_to(message, f"❌ کێشەیەک ڕوویدا: {str(e)}")

if __name__ == "__main__":
    # دەستپێکردنی سێرڤەری وێب لە باکگراوند
    t = Thread(target=run_web)
    t.start()
    # دەستپێکردنی بۆتەکە
    bot.polling(none_stop=True)
