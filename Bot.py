import asyncio
import logging
import re
import unicodedata

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "9192441518:AAFsuOfIbwti_qE4BURAGQTlSxlhwuEZUTk"

CHANNEL_USERNAME = "@krmzi_JD"
CHANNEL_LINK = "https://t.me/krmzi_JD"
REQUEST_GROUP_LINK = "https://t.me/iekekdkj"

channels_dict = {
    "انت من احب": "https://t.me/+yAwrqyu9Z9MxYjNk",
    "حب محتمل": "https://t.me/+s4bNfzIMJmZjZmY0",
    "تحت الارض": "https://t.me/+zCD3mSNC8Y9lMzY0",
    "في السابعة عشر": "https://t.me/+VvwDlzEbtT9iNzJk",
    "المعلمة أومور": "https://t.me/+405drUn8v7oxY2E0",
    "الاعراف": "https://t.me/+Td3EZl4VfdNlMDBk",
    "ورود وذنوب": "https://t.me/+HXLagJmSxTMyNGY0",
    "الخليفة": "https://t.me/kskskkuu",
    "اعلانات": "https://t.me/a1sso",
    "حب اسود": "https://t.me/+o1KH2oxwMsoyODA0",
    "احلى نصيب": "https://t.me/+H-eOV4IvizozOTE0",
    "إسطنبول راسا على عقب": "https://t.me/+QW1X6GCHZ2U5ODU0",
    "الزواج الجميل": "https://t.me/GZALDIZI",
    "قرمزي": "https://t.me/krmzi_JD",
    "حياة الاخرين": "https://t.me/HeDizi",
    "نصف الام": "https://t.me/AcDizi",
    "حبك نار": "https://t.me/SbDizi",
    "القهوة المالحة": "https://t.me/TqDizi",
    "حبي هو البحر الاسود": "https://t.me/ApDizi",
    "قصر المرجان": "https://t.me/MgDizi",
    "حيث تشرق الشمس": "https://t.me/GdDizi",
    "هذا البحر سوف يفيض": "https://t.me/TnDizi",
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

async def check_subscription(user_id, context: ContextTypes.DEFAULT_TYPE):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
    except Exception:
        pass
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_name = user.first_name or "عزيزي"
    
    is_subscribed = await check_subscription(user.id, context)
    if not is_subscribed:
        keyboard = [
            [InlineKeyboardButton("📢 اشترك في قناة قرمزي أولاً", url=CHANNEL_LINK)],
            [InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            text=f"عذراً يا {user_name} 🚫\nيجب عليك الاشتراك في قناة البوت الرسمية أولاً لتمكين استخدام البوت ⬇️",
            reply_markup=reply_markup
        )
        return

    keyboard = [
        [InlineKeyboardButton("📢 قناة قرمزي", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = (
        f"أهلاً بك يا {user_name} ✨\n\n"
        f"أهلاً بك في بوت قرمزي للبحث عن المسلسلات. أرسل اسم المسلسل الذي تبحث عنه وسأقوم بتوفيره لك ⬇️"
    )
    await update.message.reply_text(text=welcome_text, reply_markup=reply_markup)
لقد أرسلت
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    is_subscribed = await check_subscription(user.id, context)
    
    if not is_subscribed:
        keyboard = [
            [InlineKeyboardButton("📢 اشترك في قناة قرمزي أولاً", url=CHANNEL_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            text="عذراً، لا يمكنك استخدام البوت حتى تشترك في القناة الإجبارية أولاً ⬇️",
            reply_markup=reply_markup
        )
        return

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
            text="تفضل بطلبك، يمكنك الانضمام للقناة عبر الزر أدناه ⬇️",
            reply_markup=reply_markup
        )
    else:
        keyboard = [
            [InlineKeyboardButton("📌 طلب مسلسل جديد", url=REQUEST_GROUP_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            text="عذراً، المسلسل غير متوفر لدينا حالياً. يمكنك طلبه عبر الانضمام لقروب الطلبات أدناه ⬇️",
            reply_markup=reply_markup
        )

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    application.run_polling()

if _name_ == "_main_":
    main()
