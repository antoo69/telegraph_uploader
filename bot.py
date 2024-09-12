import telebot
import os
from telebot import types  # Import untuk menggunakan inline keyboard
from telegraph import Telegraph
from config import BOT_TOKEN

# Inisialisasi bot Telegram dan Telegraph
bot = telebot.TeleBot(BOT_TOKEN)
telegraph = Telegraph()

# Registrasi akun di Telegraph
telegraph.create_account(short_name='telegraph_bot')

# Folder sementara untuk menyimpan file gambar
TEMP_DIR = './temp/'

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Handler untuk perintah /start dengan Inline Keyboard
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Membuat inline keyboard
    markup = types.InlineKeyboardMarkup()
    
    # Tombol menuju channel
    channel_button = types.InlineKeyboardButton(text="Channel", url="https://t.me/YourChannelLink")  # Ganti dengan link channel kamu
    # Tombol untuk mengunggah foto ke Telegraph
    upload_button = types.InlineKeyboardButton(text="Upload", callback_data="upload_photo")
    
    # Menambahkan tombol ke markup
    markup.add(channel_button, upload_button)
    
    # Pesan sambutan
    bot.send_message(message.chat.id, "Selamat datang di *Ferdi x Bot*!\nSaya menyediakan berbagai macam bot untuk keperluan grup. "
                                      "Silakan tekan *Channel* untuk melihat bot apa saja yang saya punya, dan klik *Upload* untuk "
                                      "convert dari gambar ke link Telegraph.",
                     parse_mode='Markdown', reply_markup=markup)

# Handler untuk mengunggah foto ketika pengguna menekan tombol Upload
@bot.callback_query_handler(func=lambda call: call.data == "upload_photo")
def upload_photo_callback(call):
    bot.send_message(call.message.chat.id, "Silakan kirim gambar yang ingin diunggah ke Telegraph.")

# Handler untuk mengunggah foto
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Mengambil file foto
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Menyimpan file sementara
    file_name = TEMP_DIR + file_info.file_path.split("/")[-1]
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    # Unggah ke Telegraph
    try:
        response = telegraph.upload_file(file_name)
        telegraph_url = 'https://telegra.ph/' + response[0]['src']
        bot.reply_to(message, f"Foto berhasil diunggah! Berikut tautannya: {telegraph_url}")
    except Exception as e:
        bot.reply_to(message, f"Gagal mengunggah foto. Error: {str(e)}")
    
    # Hapus file setelah unggah
    os.remove(file_name)

# Jalankan bot
bot.polling()
