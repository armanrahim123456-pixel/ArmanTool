import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# 🔐 گرفتن توکن‌ها از Render (Environment Variables)
TOKEN = os.getenv("TOKEN")
OPENROUTER_API_KEY = os.getenv("API_KEY")

# 🤖 AI Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# 🎮 منو
keyboard = [["🤖 هوش مصنوعی"]]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 👤 کاربران فعال AI
ai_users = set()


# 🚀 استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ai_users.discard(update.effective_user.id)

    await update.message.reply_text(
        "👋 به ArmanTool خوش اومدی!\n🤖 آماده استفاده از AI هستی",
        reply_markup=markup
    )


# 🤖 AI FUNCTION
def ai_response(text):
    res = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[
            {
                "role": "system",
                "content": "تو یک دستیار هوشمند، ساده و دقیق هستی. جواب‌ها کوتاه و قابل فهم باشه."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.3,
        max_tokens=300
    )
    return res.choices[0].message.content


# ⚙️ هندل پیام‌ها
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "🤖 هوش مصنوعی":
        ai_users.add(user_id)
        await update.message.reply_text("🤖 AI فعال شد، حالا پیام بده")
        return

    if user_id in ai_users:
        try:
            reply = ai_response(text)
            await update.message.reply_text(reply)
        except Exception as e:
            await update.message.reply_text("❌ خطا در AI")
            print(e)
        return


# 🚀 اجرای بات
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle))

app.run_polling()