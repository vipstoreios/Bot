import os
import telebot
import asyncio
from mega import Mega
from flask import Flask
from threading import Thread

# ئەگەر وەشانەکە زۆر نوێ بوو، ئەم فێڵە بەکاردەهێنین بۆ چاککردنی کتێبخانەی مێگا
if not hasattr(asyncio, 'coroutine'):
    import types
    asyncio.coroutine = lambda f: f

# --- زانیارییەکانت لێرە دابنێ ---
API_TOKEN = '8400153721:AAEZ-EE3DzMmx5D_irDRq4CYWiVH9UVckyM'
MEGA_EMAIL = 'kakaado.tech@gmail.com'
MEGA_PASSWORD = 'Ostaz.kim88'

bot = telebot.TeleBot(API_TOKEN)
mega = Mega()
m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)

app = Flask('')
@app.route('/')
def home():
    return "Fly Store Bot is Live!"

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        msg = bot.reply_to(message, "⏳ خەریکی داگرتنی فایلەکەم...")
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name
        
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        bot.edit_message_text("📤 بەرزکردنەوە بۆ MEGA...", message.chat.id, msg.message_id)
        file = m.upload(file_name)
        link = m.get_upload_link(file)
        
        bot.edit_message_text(f"✅ تەواو بوو!\n\n🔗 لینک: {link}", message.chat.id, msg.message_id)
        os.remove(file_name)
    except Exception as e:
        bot.reply_to(message, f"❌ کێشە: {str(e)}")

def run_web():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    bot.polling(none_stop=True)
