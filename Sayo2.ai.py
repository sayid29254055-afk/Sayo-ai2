# Sayo-ai2
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

# 1. Configuration
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

client = OpenAI(api_key=OPENAI_API_KEY)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 2. Logical AI Response Logic
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Use OpenAI to generate a logical, helpful response
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a logical, highly intelligent AI assistant. Answer queries with reasoning and clarity."},
            {"role": "user", "content": user_text}
        ]
    )
    
    ai_reply = response.choices[0].message.content
    await update.message.reply_text(ai_reply)

# 3. Search Logic
# Note: Telegram's API doesn't allow bots to "scrape" all users for privacy.
# We use logic to direct users to global search or specific directories.
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide a name or keyword. Example: /search fitness_bot")
        return

    search_msg = (
        f"🔍 **Search Results for:** '{query}'\n\n"
        f"1. **Global Search:** [Click here to search Telegram](https://t.me/search?q={query})\n"
        f"2. **Bot Directory:** Check @BotListBot or @BotFather for official tools.\n"
        f"3. **Logical Suggestion:** If you are looking for a person, try searching their @username directly in the main search bar."
    )
    await update.message.reply_text(search_msg, parse_mode='Markdown', disable_web_page_preview=True)

# 4. Main Application Setup
if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler('start', lambda u, c: u.message.reply_text("Hello! I am your logical AI. How can I assist?")))
    application.add_handler(CommandHandler('search', search))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    application.run_polling()
