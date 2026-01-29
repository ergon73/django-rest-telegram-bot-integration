"""
Telegram-бот для интеграции с Django API.
Команды: /start, /myinfo
"""
import os
import telebot
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8010/api")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не задан в .env")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def handle_start(message: telebot.types.Message) -> None:
    """Регистрация пользователя через API."""
    user_id = message.from_user.id
    username = message.from_user.username

    try:
        response = requests.post(
            f"{API_BASE_URL}/register/",
            json={"user_id": user_id, "username": username},
            timeout=10
        )

        if response.status_code == 201:
            bot.reply_to(message, "✅ Вы успешно зарегистрированы!")
        elif response.status_code == 200:
            data = response.json()
            if data.get("already_registered"):
                bot.reply_to(message, "ℹ️ Вы уже зарегистрированы.")
            else:
                bot.reply_to(message, "✅ Регистрация подтверждена.")
        else:
            bot.reply_to(message, f"❌ Ошибка API: код {response.status_code}")

    except requests.RequestException as e:
        bot.reply_to(message, f"❌ Не удалось связаться с API: {e}")


@bot.message_handler(commands=["myinfo"])
def handle_myinfo(message: telebot.types.Message) -> None:
    """Получение информации о пользователе через API."""
    user_id = message.from_user.id

    try:
        response = requests.get(
            f"{API_BASE_URL}/user/{user_id}/",
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            info_text = (
                f"📋 Ваши данные:\n"
                f"• ID: {data.get('user_id')}\n"
                f"• Username: {data.get('username') or 'не указан'}\n"
                f"• Дата регистрации: {data.get('created_at')}"
            )
            bot.reply_to(message, info_text)
        elif response.status_code == 404:
            bot.reply_to(
                message,
                "⚠️ Вы не зарегистрированы.\nИспользуйте /start для регистрации."
            )
        else:
            bot.reply_to(message, f"❌ Ошибка API: код {response.status_code}")

    except requests.RequestException as e:
        bot.reply_to(message, f"❌ Не удалось связаться с API: {e}")


if __name__ == "__main__":
    print("🤖 Бот запущен...")
    bot.infinity_polling()
