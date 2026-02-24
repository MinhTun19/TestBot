import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

def format_account(text: str):
    parts = text.strip().split("|")

    while len(parts) < 7:
        parts.append("")

    user_id = parts[0]
    password = parts[1]
    twofa = parts[2]
    mail = parts[3]
    mail_pass = parts[4]
    second_mail = parts[5]
    cookie_full = parts[6]

    cookie_result = ""
    if "c_user=" in cookie_full and "xs=" in cookie_full:
        import re
        c_user = re.search(r'c_user=[^;]+;', cookie_full)
        xs = re.search(r'xs=[^;]+;', cookie_full)
        if c_user and xs:
            cookie_result = f"{c_user.group()}{xs.group()}"

    result = f"""help me check new profile      :
id: {user_id}
pass: {password}
2fa: {twofa}
mail: {mail}
pass mail: {mail_pass}"""

    if second_mail.strip():
        result += f"\n2nd mail: {second_mail}"

    result += f"\ncookie: {cookie_result}"
    return result


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(format_account(update.message.text))


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
