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
fire_db = db['fire']
thunder_db = db['thunder']
ice_db = db['ice']
darkness_db = db['darkness']
light_db = db['light']
wind_db = db['wind']
nature_db = db['nature']
water_db = db['water']

async def start_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    if is_member and is_member_2 and is_member.status != "left" and is_member_2.status != "left" and is_member.status != "Left" and is_member_2.status != "Left":
        hmm = infodb.find_one({"user_id":update.message.from_user.id})
        if not hmm:
            infodb.insert_one({"user_id":update.message.from_user.id})
            await update.message.reply_text("Successfully Pre register. Refer your frnds to win more rewards."
                                            f"\n\n```Link:\nhttps://t.me/YurasaniaBot?start={update.message.from_user.id}```",
                                            parse_mode=ParseMode.MARKDOWN)
            kkk =True
            if update.message.text == "/start":
                pass
            else:
                refer_db.insert_one({"user_id":update.message.from_user.id, "refered_by":int(update.message.text.split(" ")[-1])})
                await context.bot.send_message(chat_id=int(update.message.text.split(" ")[-1]), text=f"User id: {update.message.from_user.id}\n\nUsed your refer link.")
                text= f"User id: {str(update.message.from_user.id)}\n\nUsed refer link of {str(update.message.text.split(" ")[-1])}\n\n`/info {str(update.message.from_user.id)}`\n`/info {str(update.message.text.split(" ")[-1])}`"
                print(text)
                kkk=False
                await context.bot.send_message(chat_id=-1002003442244, text=text, parse_mode=ParseMode.MARKDOWN)
            if kkk:
            	await context.bot.send_message(chat_id=-1002003442244, text=f"User id: {str(update.message.from_user.id)}\n\n`/info {str(update.message.from_user.id)}`", parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text("You have already pre-registered.")
    else:
        keyboard = [[InlineKeyboardButton("Channel", url="https://t.me/Yurasania"), InlineKeyboardButton("Group", url="https://t.me/YurasaniaChat")]]
        await update.message.reply_text("Please join the following channel and use the command again to start.", reply_markup=InlineKeyboardMarkup(keyboard))

async def preregcount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    x = infodb.find({})
    count = len(list(x))
    await update.message.reply_text(f"Total no. of user who pre-registered: {count}")

async def newpoll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == 1037179104:
        splitd = update.message.split(" ")
        user_id = splitd[0]
        uname = splitd[1]
        king = splitd[2]
        if king.lower() in ["darkness", "thunder", "light", "water", "wind", "nature", "ice", "fire"]
            text = "*King of {}*\nUser id: `{}`\nUsername: {}".format(king.title(), user_id, uname)
            keyboard = [[InlineKeyboardButton("Channel", callback_data=f"vote|{user_id}|{king}"]]
            await update.message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard)) # chat_id=-1002102617074, 
            await update.message.reply_text(f"Test phase Success")
        else:
            await update.message.reply_text("tell correct element")        

def main() -> None:
    application = Application.builder().token("7027271738:AAHwridfxHokuSJ53B-j8S0u5bstI5gtq4Y").concurrent_updates(
        256).rate_limiter(AIORateLimiter(max_retries=30)).build()
    application.add_handler(CommandHandler("start", start_func))
    application.add_handler(CommandHandler("precount", preregcount))
    application.add_handler(CommandHandler("new", send))
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
