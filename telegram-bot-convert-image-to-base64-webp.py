import telebot
import os
from PIL import Image
import base64
import time
from datetime import datetime

bot = telebot.TeleBot('YOUR_TOKEN_HERE')

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Convert image to webp and webp to base64. Limit size 20 Mb.')

@bot.message_handler(content_types='photo')
def handle_file3(message):
    chat_id = message.chat.id
    user_photo_id = message.photo[-1].file_id
    file_photo = bot.get_file(user_photo_id)
    filename, file_extension = os.path.splitext(file_photo.file_path)
    downloaded_file_photo = bot.download_file(file_photo.file_path)
    src = user_photo_id + file_extension
    try:
        with open(src,'wb') as new_file:
            new_file.write(downloaded_file_photo)
        time.sleep(1)
        bot.send_message(chat_id, text='Loading...')
        im = Image.open(user_photo_id + file_extension).convert("RGB")
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.webp'
        im.save(('/' + filename),'webp', quality=90)
        time.sleep(1)
        bot.send_message(chat_id, text='Convert to webp...')
        time.sleep(1)
        with open(('/' + filename.replace('.webp', '.txt')), "w") as f1:
            with open(('/' + filename), "rb") as img_file:
                b64_string = base64.b64encode(img_file.read())
                bas64 = (b64_string.decode('utf-8'))
                f1.write(bas64)
        time.sleep(1)
        bot.send_message(chat_id, text='Convert to base64 ...')
        time.sleep(1)
        with open('/' + filename.replace('.webp', '.txt'), 'rb') as f:
            bot.send_document(chat_id, f)

        with open('/' + filename, "rb") as img_file:
            bot.send_document(chat_id, img_file)
        time.sleep(1)
        os.remove(src)
        time.sleep(1)
        os.remove('/' + filename)
        bot.send_message(chat_id, text='Del temp files')
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        bot.send_message(chat_id, text=error_msg)

if __name__ == '__main__':
     bot.polling(none_stop=True)
