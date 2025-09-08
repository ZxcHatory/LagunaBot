import telebot
from flask import Flask, request
import os

# Получаем токен бота из переменной окружения или используем указанный
BOT_TOKEN = os.getenv('BOT_TOKEN', '8205199189:AAEZRBgPMUNXnqJFNgfsme5fB5HJtYX3CiQ')
# Замени 'YOUR_ADMIN_CHAT_ID' на свой ID чата
# Чтобы узнать ID, напиши @userinfobot и он пришлёт твой ID
ADMIN_CHAT_ID = 5630139705

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправляй мне анонимные сообщения, и я перешлю их админам канала ХПЕ. 💭😉")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Получаем информацию о пользователе
        user = message.from_user
        full_name = user.first_name
        if user.last_name:
            full_name += f" {user.last_name}"
        
        username = f"@{user.username}" if user.username else "без никнейма"
        user_id = user.id
        
        # Формируем сообщение с информацией о пользователе
        user_info = f"👤 От: {full_name}\n🏷 Никнейм: {username}\n🆔 ID: {user_id}\n\n📝 Сообщение:\n{message.text}"
        
        # Пересылка сообщения с информацией о пользователе
        bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=user_info
        )
        # Ответ пользователю, чтобы он знал, что сообщение отправлено
        bot.reply_to(message, "Твоё сообщение было отправлено, жди пока его запостят в канале ! 🐝.")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Произошла ошибка. Попробуй ещё раз.")

# Главная страница для проверки статуса бота
@app.route('/')
def index():
    return '''
    <h1>🤖 LagunaAnon Bot</h1>
    <p>✅ Бот активен и работает</p>
    <p>📱 Найдите бота в Telegram и начните отправлять анонимные сообщения</p>
    <p>🔗 Webhook настроен правильно</p>
    '''

# Настройка веб-сервера для работы бота
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

if __name__ == "__main__":
    # Получаем домен Replit
    replit_domain = os.getenv('REPLIT_DEV_DOMAIN', 'localhost')
    
    # Устанавливаем webhook только если мы не на localhost
    if replit_domain != 'localhost':
        webhook_url = f'https://{replit_domain}/{BOT_TOKEN}'
        try:
            bot.set_webhook(url=webhook_url)
            print(f"Webhook установлен: {webhook_url}")
        except Exception as e:
            print(f"Ошибка установки webhook: {e}")
    else:
        print("Запуск в режиме polling (локальная разработка)")
        bot.remove_webhook()
    
    print("Запуск Flask сервера...")
    app.run(host='0.0.0.0', port=5000)
