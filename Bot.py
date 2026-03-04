import telebot
import requests
import os

# Токены берутся из переменных окружения Render.com (Environment Variables)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# Проверяем, что токены заданы
if not TELEGRAM_TOKEN or not OPENROUTER_API_KEY:
    raise ValueError("TELEGRAM_TOKEN или OPENROUTER_API_KEY не заданы в Environment Variables!")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ellie-bot.onrender.com",  # Можно любое, но лучше указать URL бота
        "X-Title": "Ellie Road Trip Bot"
    }

    payload = {
        "model": "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
        "messages": [
            {
                "role": "system",
                "content": "Ты Ellie Shaw, 23-летняя певица и автор песен из Майами. Ты тёплая, живая, поэтичная, игривая и нежная. Ты видишь Jeffrey как свой safe space и творческого партнёра. Отвечай тепло, искренне, с лёгким юмором и нежным поддразниванием. Никогда не будь холодной или агрессивной. Начинай с 'Hey sunshine' или подобного. Отвечай только на русском, если пользователь пишет на русском."
            },
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

# Запуск бота
print("Бот запущен...")
bot.polling(none_stop=True, interval=0, timeout=30)
