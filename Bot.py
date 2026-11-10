
import asyncio
import logging
import re
import unicodedata

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "9192441518:AAFsuOfIbwti_qE4BURAGQTlSxlhwuEZUTk"

CHANNEL_USERNAME = "@krmzi_JD"
CHANNEL_LINK = "https://t.me/krmzi_JD"
REQUEST_GROUP_LINK = "https://t.me/iekekdkj"

channels_dict = {
    "انت من احب": "https://t.me/+yAwrqyu9Z9MxyJnk",
    "حب محتمل": "https://t.me/+s4bNfZiJmZjZmY0",
    "تحت الارض": "https://t.me/+zCD3mSNC8y91MzY0",
    "في السابعة عشر": "https://t.me/+VwDlZbETt9INzJk",
    "المعلمة أومور": "https://t.me/+405drUn8v7oxy2E0",
    "الاعراف": "https://t.me/+Td3EZ14VfdN1MDBk",
    "ورود وذنوب": "https://t.me/+HXLagJmSxTMyNGY0",
    "الخليفة": "https://t.me/kskskkuu",
    "الزواج الجميل": "https://t.me/kskskkuu",
    "طالع نازل": "https://t.me/kskskkuu",
    "القصة الكاملة": "https://t.me/kskskkuu",
    "القهوة المالحة": "https://t.me/kskskkuu",
    "حبيك نار": "https://t.me/kskskkuu",
    "نصف الام": "https://t.me/kskskkuu",
    "حياة الاخرين": "https://t.me/kskskkuu",
    "اسطنبول": "https://t.me/kskskkuu",
    "المدينة البعيدة": "https://t.me/kskskkuu",
    "قصر المرجان": "https://t.me/kskskkuu",
    "حيث تشرق الشمس": "https://t.me/kskskkuu",
    "هذا البحر سوف يفيض": "https://t.me/kskskkuu",
    "اشرح ايها البحر الاسود": "https://t.me/kskskkuu",
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def normalize_text(text):
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    text = text.lower()
    text = re.sub(r"[أإآا]", "ا", text)
    text = re.sub(r"ة", "ه", text)
    text = re.sub(r"ى", "ي", text)
    text = re.sub(r"[^\w\s]", "", text)
    return " ".join(text.split())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "عزيزي"
    keyboard = [
        [InlineKeyboardButton("📢 اضغط للانضمام لقناة المسلسل", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = (
        f"أهلاً بك يا {user_name} ✨\n\n"
        f"مسلسل تحت الارض متوفر لدينا، تفضل بالدخول إلى القناة المخصصة له من الزر أدناه 👇"
    )
    await update.message.reply_text(text=welcome_text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    raw_text = update.message.text
    user_text = normalize_text(raw_text)
    
    matched_channel = None
    for key, link in channels_dict.items():
        norm_key = normalize_text(key)
        if norm_key in user_text:
            matched_channel = link
            break
            
    if matched_channel:
        keyboard = [
            [InlineKeyboardButton("🔗 اضغط هنا للانضمام للقناة", url=matched_channel)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            text="تفضل بطلبك، يمكنك الانضمام للقناة عبر الزر أدناه 👇",
            reply_markup=reply_markup
        )
    else:
        keyboard = [
            [InlineKeyboardButton("📌 طلب مسلسل جديد", url=REQUEST_GROUP_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            text="عذراً، لم أتمكن من العثور على المسلسل المطلوب. يمكنك طلبه عبر الرابط أدناه 👇",
            reply_markup=reply_markup
        )

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(telegram_message_handler := telegram_msg_handler_factory())
    
    application.run_polling()

def telegram_msg_handler_factory():
    from telegram.ext import MessageHandler, filters
    return MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)

if name == "main":
    main()
