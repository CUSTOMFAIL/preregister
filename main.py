import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, AIORateLimiter, \
    CallbackQueryHandler
from telegram.constants import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from pymongo import MongoClient
import asyncio
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
        link= await context.bot.create_chat_invite_link(chat_id=-1001763955719, member_limit=1,
                                                      name=update.message.from_user.id)
        keyboard = [[InlineKeyboardButton("Channel", url="https://t.me/Yurasania"), InlineKeyboardButton("Group", url=link.invite_link)]]
        await update.message.reply_text("Please join the following channel and use the command again to start.", reply_markup=InlineKeyboardMarkup(keyboard))

async def preregcount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    x = infodb.find({})
    count = len(list(x))
    await update.message.reply_text(f"Total no. of user who pre-registered: {count}")

async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        if hmm:
            has_ref = refer_db.find_one({"user_id":update.message.from_user.id})
            if not has_ref:
                splitd = update.message.text.split(" ", 1)
                twtuser = splitd[1]
                refer_db.insert_one({"user_id":update.message.from_user.id, "refered_by":int(twtuser)})
                await update.message.reply_text("Successfully referred")
            else:
                await update.message.reply_text("You have already referred someone")
        else:
            await update.message.reply_text("You havent pre registered yet.")
    else:
        await update.message.reply_text("Join Channel and Group first.")


async def myref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = list(refer_db.find({"refered_by":update.message.from_user.id}))
    await update.message.reply_text(f"You have refered {len(count)} users.")
                
                
    

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == 1037179104:
        if update.message.reply_to_message:
            hmm = list(infodb.find())
            biglst = [hmm[i:i+5] for i in range(0, len(hmm), 5)]
            dd = 0
            for sublst in biglst:
                for itm in sublst:
                    try:
                        await context.bot.forward_message(chat_id=int(itm['user_id']), from_chat_id=update.message.chat.id, message_id=update.message.reply_to_message.message_id)
                        dd+=1
                    except Exception as e:
                        print(e)
                    await asyncio.sleep(1)

async def newpoll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == 1037179104:
        splitd = update.message.text.split(" ")
        user_id = splitd[1]
        uname = splitd[2]
        king = splitd[3]
        if king.lower() in ["darkness", "thunder", "light", "water", "wind", "nature", "ice", "fire"]:
            text = "*King of {}*\nUser id: `{}`\nUsername: {}".format(king.title(), user_id, uname)
            keyboard = [[InlineKeyboardButton("Vote - 0", callback_data=f"vote|{user_id}|{king}|0")]]
            await context.bot.send_message(chat_id=-1002102617074, text=text.replace("_", "\_"), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN) # chat_id=-1002102617074, 
            await update.message.reply_text(f"Done")
        else:
            await update.message.reply_text("tell correct element")     

async def button_cbs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_member = False
    is_member_2 = False
    try:
        is_member = await context.bot.get_chat_member(chat_id=-1002102617074, user_id=update.callback_query.from_user.id)
    except:
        pass
    try:
        is_member_2 = await context.bot.get_chat_member(chat_id=-1001763955719, user_id=update.callback_query.from_user.id)
    except:
        pass
    if is_member and is_member_2 and is_member.status != "left" and is_member_2.status != "left" and is_member.status != "Left" and is_member_2.status != "Left":
        hmm = infodb.find_one({"user_id":update.callback_query.from_user.id})
        if hmm:
            splitd = update.callback_query.data.split("|")
            element = splitd[2]
            has_voted = db[element.lower()].find_one({"user_id":update.callback_query.from_user.id})
            voting_whom = splitd[1]
            total_votes = int(splitd[3])
            if update.callback_query.from_user.id == 1037179104:
                ggg = list(db[element.lower()].find({"whom":int(voting_whom)}))
                keyboard = [[InlineKeyboardButton(f"Vote - {len(ggg)}", callback_data=f"vote|{voting_whom}|{element}|{total_votes}")]]
                await update.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
            if has_voted:
                if int(voting_whom) == int(has_voted['whom']):
                    await update.callback_query.answer("You have already vote this person")
                    return None
                await update.callback_query.answer("You have already voted. You cant change your vote")
            else:   
                db[element.lower()].insert_one({"user_id":update.callback_query.from_user.id, "whom":int(voting_whom)})
                ggg = list(db[element.lower()].find({"whom":int(voting_whom)}))
                print(len(ggg))
                keyboard = [[InlineKeyboardButton(f"Vote - {len(ggg)}", callback_data=f"vote|{voting_whom}|{element}|{total_votes+1}")]]
                await update.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))
                await update.callback_query.answer("You have successfully voted.")
        else:
            await update.callback_query.answer("Pre register in bot before voting") 
    else:
        await update.callback_query.answer("Join channel and discussion to give vote")

    

def main() -> None:
    application = Application.builder().token("7027271738:AAHwridfxHokuSJ53B-j8S0u5bstI5gtq4Y").concurrent_updates(
        256).rate_limiter(AIORateLimiter(max_retries=30)).build()
    application.add_handler(CommandHandler("start", start_func))
    application.add_handler(CommandHandler("precount", preregcount))
    application.add_handler(CommandHandler("new", newpoll))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("refer", refer))
    application.add_handler(CommandHandler("myref", myref))
    application.add_handler(CallbackQueryHandler(button_cbs))
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
