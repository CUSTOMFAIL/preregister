import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, AIORateLimiter, \
    CallbackQueryHandler
from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from pymongo import MongoClient
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger('apscheduler').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

basic_info_db_url = ("mongodb+srv://customfailure00006:customfailure00006@preregister.5tar1aa.mongodb.net/?retryWrites=true&w=majority&appName=preregister")
cluster = MongoClient(basic_info_db_url)
db = cluster["gamebot"]
infodb = db["pre_reg"]
refer_db = db['refer']

async def start_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(True)
    is_member = False
    is_member_2 = False
    try:
        is_member = await context.bot.get_chat_member(chat_id=-1002102617074, user_id=update.message.from_user.id)
    except:
        pass
    try:
        is_member_2 = await context.bot.get_chat_member(chat_id=-1001763955719, user_id=update.message.from_user.id)
    except:
        pass
    print(is_member_2.status)
    if is_member_2.status == "LEFT" or is_member_2.status == "left":
        print("Left")
    print(is_member.status)
    if is_member.status == "LEFT" or is_member.status == "left":
        print("Left")
    if is_member and is_member_2 and is_member.status != "left" and is_member_2.status != "left" and is_member.status != "Left" and is_member_2.status != "Left":
        hmm = infodb.find_one({"user_id":update.message.from_user.id})
        if not hmm:
            infodb.insert_one({"user_id":update.message.from_user.id})
            await update.message.reply_text("Successfully Pre register. Refer your frnds to win more rewards."
                                            f"\n\n```Link:\nhttps://t.me/YurasaniaBot?start={update.message.from_user.id}```",
                                            parse_mode=ParseMode.MARKDOWN)
            if update.message.text == "/start":
                pass
            else:
                refer_db.insert_one({"user_id":update.message.from_user.id, "refered_by":int(update.message.text.split(" ")[-1])})
                await context.bot.send_message(chat_id=int(update.message.text.split(" ")[-1]), text=f"User id: {update.message.from_user.id}\n\nUsed your refer link.")
                text= f"User id: {str(update.message.from_user.id)}\n\nUsed refer link of {str(update.message.text.split(" ")[-1])}\n\n`/info {str(update.message.from_user.id)}`\n`/info {str(update.message.text.split(" ")[-1])}`"
                print(text)
                await context.bot.send_message(chat_id=-1002003442244, text=text, parse_mode=ParseMode.MARKDOWN)
            await context.bot.send_message(chat_id=-1002003442244, text=f"User id: {str(update.message.from_user.id)}\n\n`/info {str(update.message.from_user.id)}`", parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text("You have already pre-registered.")
    else:
        keyboard = [[InlineKeyboardButton("Channel", url="https://t.me/Yurasania"), InlineKeyboardButton("Group", url="https://t.me/YurasaniaChat")]]
        await update.message.reply_text("Please join the following channel and use the command again to start.", reply_markup=InlineKeyboardMarkup(keyboard))

def main() -> None:
    application = Application.builder().token("7027271738:AAHwridfxHokuSJ53B-j8S0u5bstI5gtq4Y").concurrent_updates(
        256).rate_limiter(AIORateLimiter(max_retries=30)).build()
    application.add_handler(CommandHandler("start", start_func))
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
