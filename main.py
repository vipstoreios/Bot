import os
import telebot
from mega import Mega
from flask import Flask
from threading import Thread

# --- زانیارییەکان ---
API_TOKEN = '8400153721:AAEZ-EE3DzMmx5D_irDRq4CYWiVH9UVckyM'
MEGA_EMAIL = 'kakaado.tech@gmail.com'
MEGA_PASSWORD = 'Ostaz.kim88'

bot = telebot.TeleBot(API_TOKEN)

def upload_to_mega(file_path):
    try:
        mega = Mega()
        m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)
        file = m.upload(file_path)
        return m.get_upload_link(file)
    except Exception as e:
        return f"Error: {str(e)}"

app = Flask('')
@app.route('/')
def home():
    return "Bot is Running!"

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    msg = bot.reply_to(message, "⏳ خەریکی داگرتنی فایلەکەم لە تەلەگرام...")
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = message.document.file_name
    
    with open(file_name, 'wb') as f:
        f.write(downloaded_file)
        
    bot.edit_message_text("📤 ئێستا بەرز دەکرێتەوە بۆ MEGA...", message.chat.id, msg.message_id)
    link = upload_to_mega(file_name)
    
    bot.edit_message_text(f"✅ تەواو بوو!\n\n🔗 لینک: {link}", message.chat.id, msg.message_id)
    os.remove(file_name)

def run_web():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    bot.polling(none_stop=True)
