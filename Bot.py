import asyncio
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# إعداد السجلات
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# اليوزر أو المعرف الخاص بقناة قرمزي الإجبارية (بدون رابط، فقط اليوزر مع @)
# بما أن رابط قناتك هو https://t.me/krmzi_JD إذن يوزرها هو @krmzi_JD
CHANNEL_USERNAME = "@krmzi_JD"
CHANNEL_LINK = "https://t.me/krmzi_JD"

# رابط قروب الطلبات الجديد
REQUEST_GROUP_LINK = "https://t.me/iekekdkj"

# قاموس المسلسلات والروابط
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
    "إسطنبول رأساً على عقب": "https://t.me/+QW1X6GCHZ2U5ODU0",
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


# دالة للتحقق إذا كان العضو مشترك في القناة أو لا
async def check_subscription(user_id, context):
  try:
    member = await context.bot.get_chat_member(
        chat_id=CHANNEL_USERNAME, user_id=user_id
    )
    # حالات المشترك الفعلي في التليجرام
    if member.status in ["member", "administrator", "creator"]:
      return True
  except Exception:
    pass
  return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_user.id
  user_name = update.effective_user.first_name

  # فحص الاشتراك الإجباري أول ما يفتح البوت
  is_subscribed = await check_subscription(user_id, context)

  if not is_subscribed:
    reply_text = (
        f"أهلاً بك {user_name} 🌸\nعذراً, لا يمكنك استخدام البوت إلا بعد الانضمام"
        f" إلى قناة قرمزي الأساسية ⬇️\n\n(الرابط فقط لمدة دقيقة واحدة)"
    )
    keyboard = [
        [InlineKeyboardButton("اشترك في قناة قرمزي 📢", url=CHANNEL_LINK)],
        [InlineKeyboardButton("قروب الطلبات 💬", url=REQUEST_GROUP_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    sent_message = await update.message.reply_text(
        reply_text, reply_markup=reply_markup
    )
  else:
    await update.message.reply_text(
        f"أهلاً بك {user_name} في بوت قرمزي للبحث عن المسلسلات 🎬\nأرسل اسم"
        " المسلسل وابحث عنه الآن!"
    )

s
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_user.id
  user_name = update.effective_user.first_name
  text = update.message.text.strip().lower()

  # فحص الاشتراك الإجباري مع كل رسالة يرسلها العضو
  is_subscribed = await check_subscription(user_id, context)

  if not is_subscribed:
    reply_text = (
        f"عذراً {user_name} ❌\nيجب عليك الاشتراك في قناة قرمزي لتتمكن من استخدام"
        f" البوت والبحث عن المسلسلات ⬇️\n\n(الرابط فقط لمدة دقيقة واحدة)"
    )
    keyboard = [
        [InlineKeyboardButton("اشترك في قناة قرمزي 📢", url=CHANNEL_LINK)],
        [InlineKeyboardButton("قروب الطلبات 💬", url=REQUEST_GROUP_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    sent_message = await update.message.reply_text(
        reply_text, reply_markup=reply_markup
    )
# حذف رسالة التنبيه بعد دقيقة
    async def delete_later():
      await asyncio.sleep(60)
      try:
        await sent_message.delete()
      except Exception:
        pass

    asyncio.create_task(delete_later())
    return

  # تنظيف النص لو كتب العضو كلمة "مسلسل"
  text = text.replace("مسلسل", "").strip()

  # البحث عن المسلسل
  found_link = None
  for key, link in channels_dict.items():
    if key in text:
      found_link = link
      break

  if found_link:
    reply_text = (
        f"أهلاً {user_name}\nمسلسلك متوفر، انضم للقناة ⬇️\n\n(الرابط فقط لمدة"
        " دقيقة واحدة)"
    )
    keyboard = [[InlineKeyboardButton("رابط القناة (للإنضمام)", url=found_link)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    sent_message = await update.message.reply_text(
        reply_text, reply_markup=reply_markup
    )
  else:
    reply_text = (
        f"مسلسلك للأسف غير متوفر، انضم لقروب الطلبات ويرسل لك المشرف وقت فتحه"
        f" ⬇️\n\n(الرابط فقط لمدة دقيقة واحدة)"
    )
    keyboard = [
        [InlineKeyboardButton("قروب الطلبات (للإنضمام)", url=REQUEST_GROUP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    sent_message = await update.message.reply_text(
        reply_text, reply_markup=reply_markup
    )

  # حذف الرسالة بعد دقيقة واحدة
  async def delete_later():
    await asyncio.sleep(60)
    try:
      await sent_message.delete()
    except Exception:
      pass

  asyncio.create_task(delete_later())


def main():
  TOKEN = "9192441518:AAFsuOfIbwti_qE4BURAGQTlSxlhwuEZUTk"

  application = ApplicationBuilder().token(TOKEN).build()

  application.add_handler(CommandHandler("start", start))
  application.add_handler(
      MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
  )

  print("Bot is running with forced subscription...")
  application.run_polling()


if name == "main":
  main()