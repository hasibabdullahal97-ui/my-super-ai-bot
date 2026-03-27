import logging
import requests
import urllib.parse
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Configuration
BOT_TOKEN = '8324151492:AAEOoTRmYHsbtBz1jmWDkWNG923vW63wywg'
API_BASE_URL = "https://ayaanmods.site/aiimage.php?key=annonymousai&prompt="
OWNER_NAME = "Abdullah Al Hasib 313"
OWNER_USERNAME = "@abdullah_al_hasib_313"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = f"🌟 <b>Welcome!</b>\n👤 <b>Powered by:</b> {OWNER_NAME}\n🔗 <b>Contact:</b> {OWNER_USERNAME}\n\nJust send me a prompt to generate an image!"
    await update.message.reply_text(welcome, parse_mode='HTML')

async def handle_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    enhanced_prompt = f"{user_prompt}, 4k resolution, cinematic lighting, masterpiece, 8k, highly detailed"
    safe_prompt = urllib.parse.quote(enhanced_prompt)
    
    status_msg = await update.message.reply_text("✨ <b>Creating your masterpiece...</b> 🖌️", parse_mode='HTML')
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.UPLOAD_PHOTO)

    try:
        response = requests.get(f"{API_BASE_URL}{safe_prompt}", timeout=60)
        data = response.json()
        if data.get("success") and data.get("images"):
            for url in data["images"][:2]: # ৩টার বদলে ২টা ইমেজ দিচ্ছি স্পিড বাড়ানোর জন্য
                caption = f"✅ <b>Done!</b>\n📝 <b>Prompt:</b> {user_prompt[:50]}...\n👤 <b>By:</b> {OWNER_NAME}"
                await update.message.reply_photo(photo=url, caption=caption, parse_mode='HTML')
            await status_msg.delete()
        else:
            await status_msg.edit_text("❌ Failed to generate image. Try another prompt.")
    except Exception as e:
        await status_msg.edit_text("⚠️ API Error! Please try again later.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_prompt))
    application.run_polling()
