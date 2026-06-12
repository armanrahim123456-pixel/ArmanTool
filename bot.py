import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# ======================
# 🔐 ENV VARIABLES (Railway)
# ======================
TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")

# ======================
# 🤖 OpenRouter Client
# ======================
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

# ======================
# 🎮 Keyboard
# ======================
keyboard = [["🤖 هوش مصنوعی"]]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

ai_users = set()

# ======================
# 🚀 Start
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ai_users.discard(update.effective_user.id)

    await update.message.reply_text(
        "👋 به ArmanTool خوش اومدی!\n🤖 AI آماده است",
        reply_markup=markup
    )

# ======================
# 🤖 AI Function
# ======================
def ai_response(text):
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct",
            messages=[
                {"role": "system", "content": "تو یک دستیار ساده و دقیق هستی."},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(e)
        return "❌ خطا در ارتباط با AI"

# ======================
# ⚙️ Message Handler
# ======================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "🤖 هوش مصنوعی":
        ai_users.add(user_id)
        await update.message.reply_text("🤖 AI فعال شد، پیام بده")
        return

    if user_id in ai_users:
        reply = ai_response(text)
        await update.message.reply_text(reply)

# ======================
# 🚀 Main
# ======================
def main():
    if not TOKEN:
        print("❌ TOKEN is missing")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle))

    print("Bot is running...")
    app.run_polling()

if name == "main":
    main()