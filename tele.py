import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import json

TELEGRAM_BOT_TOKEN = "7349787531:AAELBLmwkRnqlmfgQoMH81rVLnihKLo31B0"
TOGETHER_API_KEY = "1200b5dd271649ae98e189601a8485af8e5092b1f456fd240c6e1e7c09e86735"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm your chatbot. How can I help you today?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    bot_response = get_bot_response(user_message)
    await update.message.reply_text(bot_response)

def get_bot_response(message):
    try:
        response = requests.post(
            'https://api.together.xyz/v1/chat/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {TOGETHER_API_KEY}'
            },
            json={
                "model": "meta-llama/Llama-2-70b-chat-hf",
                "messages": [{"role": "user", "content": message}],
                "max_tokens": 512,
                "temperature": 0.7,
                "top_p": 0.7,
                "top_k": 50,
                "repetition_penalty": 1.0,
                "stop": None  # Changed from [""] to None
            }
        )
        
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I encountered an error."

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
