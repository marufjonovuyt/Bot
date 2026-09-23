import telebot
from telebot import types
import qrcode
import os

TOKEN = "8760212213:AAEmcFCTTsGTTKGi4bS0V2Vj5vts_VgzuDw"
bot = telebot.TeleBot(TOKEN)

user_state = {}

# ===== MENU =====
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🔳 QR kod yaratish")
    kb.add("ℹ️ Bot haqida")
    return kb

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "👋 Assalomu alaykum!\n"
        "Men QR kod yasab beraman.\n"
        "Quyidagi tugmani bosing:",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "🔳 QR kod yaratish")
def ask_text(msg):
    user_state[msg.chat.id] = "qr"
    bot.send_message(msg.chat.id, "✍️ QR kodga aylantiriladigan matn yoki link yuboring:")

@bot.message_handler(func=lambda m: m.text == "ℹ️ Bot haqida")
def about(msg):
    bot.send_message(
        msg.chat.id,
        "🤖 QR Code Maker Bot\n"
        "📌 Matn yoki linkdan QR kod yaratadi\n"
        "👨‍💻 Muallif: Abdullajon"
    )

@bot.message_handler(func=lambda m: True)
def make_qr(msg):
    if user_state.get(msg.chat.id) == "qr":
        data = msg.text

        img = qrcode.make(data)
        file_name = f"qr_{msg.chat.id}.png"
        img.save(file_name)

        with open(file_name, "rb") as photo:
            bot.send_photo(msg.chat.id, photo, caption="✅ Mana sizning QR kodingiz")

        os.remove(file_name)
        user_state[msg.chat.id] = None
    else:
        bot.send_message(msg.chat.id, "❗ Iltimos, menyudan foydalaning", reply_markup=main_menu())

print("🤖 QR Code bot ishga tushdi...")
bot.infinity_polling()