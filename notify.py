import os
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_alert(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("[ALERTA SEM TELEGRAM] " + message)
        return
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)
        print(f"[TELEGRAM ENVIADO] {message}")
    except Exception as e:
        print(f"[ERRO TELEGRAM] {e}")
