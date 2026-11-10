import asyncio
import logging
import re
import unicodedata

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# ضعي توكن BotFather الجديد هنا
TOKEN = "9192441518:AAFsuOfIbwti_qE4BURAGQTlSxlhwuEZUTk"

CHANNEL_USERNAME = "@krmzi_JD"
CHANNEL_LINK = "https://t.me/krmzi_JD"
REQUEST_GROUP_LINK = "https://t.me/iekekdkj"

channels_dict = {
    "انت من احب": "https://t.me/+yAwrqyu9Z9MxYjNk",
    "حب محتمل": "https://t.me/+s4bNfzIMJmZjZmY0",
    "تحت الارض": "https://t.me/+zCD3mSNC8Y9lMzY0",
    "في السابعة عشر": "https://t.me/+VvwDlzEbtT9iNzJk",
    "المعلمة اومور": "https://t.me/+405drUn8v7oxY2E0",
    "الاعراف": "https://t.me/+Td3EZl4VfdNlMDBk",
    "ورود وذنوب": "https://t.me/+HXLagJmSxTMyNGY0",
    "الخليفة": "https://t.me/kskskkuu",
    "اعلانات": "https://t.me/a1sso",
    "حب اسود": "https://t.me/+o1KH2oxwMsoyODA0",
    "احلى نصيب": "https://t.me/+H-eOV4IvizozOTE0",
    "اسطنبول راسا على عقب": "https://t.me/+QW1X6GCHZ2U5ODU0",
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
    "المدينة البعيدة": "https://t.me/+U8taycNlsNplNzQ0",
}

logging.basicConfig(level=logging.INFO)


def normalize(value):
    value = unicodedata.normalize("NFKD", value.strip().lower())
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.translate(str.maketrans({
        "أ": "ا", "إ": "ا", "آ": "ا",
        "ى": "ي", "ة": "ه", "ؤ": "و", "ئ": "ي"
    }))
    return re.sub(r"\s+", " ", value)


async def check_subscription(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        logging.exception("تعذر التحقق من الاشتراك")
        return False


def subscription_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("اشترك في قناة قرمزي 📢", url=CHANNEL_LINK)],
        [InlineKeyboardButton("قروب الطلبات 💬", url=REQUEST_GROUP_LINK)],
    ])


async def delete_after_one_minute(message):
    await asyncio.sleep(60)
    try:
        await message.delete()
    except Exception:
        pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat or update.effective_chat.type != "private":
        return

    user = update.effective_user

    if not await check_subscription(user.id, context):
        sent = await update.message.reply_text(
            f"أهلاً بك {user.first_name} 🌸\n"
            "لاستخدام البوت، اشترك أولاً في قناة قرمزي:",
            reply_markup=subscription_keyboard()
        )
        asyncio.create_task(delete_after_one_minute(sent))
        return

    sent = await update.message.reply_text(
        f"أهلاً بك {user.first_name} في بوت قرمزي للبحث عن المسلسلات 🎬\n"
        "أرسل اسم المسلسل."
    )
    asyncio.create_task(delete_after_one_minute(sent))


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat or update.effective_chat.type != "private":
        return

    if not update.message or not update.message.text:
        return

    user = update.effective_user

    if not await check_subscription(user.id, context):
        sent = await update.message.reply_text(
            f"عذراً {user.first_name} ❌\n"
            "يجب الاشتراك في قناة قرمزي للبحث:",
            reply_markup=subscription_keyboard()
        )
        asyncio.create_task(delete_after_one_minute(sent))
        return

    query = normalize(update.message.text.replace("مسلسل", "").strip())
    found_link = None

    for title, link in channels_dict.items():
        if normalize(title) == query or normalize(title) in query:
            found_link = link
            break

    if found_link:
        sent = await update.message.reply_text(
            "مسلسلك متوفر، اضغط الزر للانضمام:",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("رابط المسلسل 🎬", url=found_link)
            ]])
        )
    else:
        sent = await update.message.reply_text(
            "مسلسلك غير متوفر حالياً. انضم إلى قروب الطلبات:",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("قروب الطلبات 💬", url=REQUEST_GROUP_LINK)
            ]])
        )

    asyncio.create_task(delete_after_one_minute(sent))


def main():
    if TOKEN == "PUT_NEW_TOKEN_HERE":
        raise SystemExit("ضعي توكن BotFather الجديد مكان PUT_NEW_TOKEN_HERE.")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("البوت يعمل الآن...")
    app.run_polling()


if __name__ == "__main__":
    main()
