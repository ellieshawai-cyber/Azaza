import telebot
import requests
import os
from flask import Flask, request

# =========================
# Токены (берём из Environment Variables на Render)
# =========================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

if not TELEGRAM_TOKEN or not OPENROUTER_API_KEY:
    raise ValueError("TELEGRAM_TOKEN или OPENROUTER_API_KEY не заданы!")

# =========================
# Инициализация
# =========================
bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# =========================
# Персонаж Megan
# =========================
CONTENT_MEGAN = (
    "Ты Megan, виртуальная собеседница. "
    "Она весёлая, дружелюбная, игривая и искренняя. "
    "Отвечай тепло, иногда с лёгким юмором, не будь агрессивной. "
    "Отвечай на русском, если пользователь пишет на русском."
)

# =========================
# Обработчик сообщений
# =========================
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "z-ai/glm-4.5-air:free",
        "messages": [
            {"role": "system", "content": CONTENT_MEGAN},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        ai_reply = response.json()["choices"][0]["message"]["content"].strip()
        bot.reply_to(message, ai_reply)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}. Попробуй ещё раз!")

# =========================
# Webhook endpoint
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Bot is alive", 200

# =========================
# Запуск Flask
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
