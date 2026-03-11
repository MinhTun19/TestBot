from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

import os

TOKEN = os.getenv("BOT_TOKEN")

def format_account(text: str):
    parts = text.strip().split("|")

    while len(parts) < 7:
        parts.append("")

    user_id, password, twofa, mail, mail_pass, second_mail, cookie_full = parts

    import re
    c_user = re.search(r'c_user=[^;]+;', cookie_full)
    xs = re.search(r'xs=[^;]+;', cookie_full)

    cookie_result = ""
    if c_user and xs:
        cookie_result = f"{c_user.group()}{xs.group()}"

    result = f"""help me check new profile :
id: {user_id}
pass: {password}
2fa: {twofa}
mail: {mail}
pass mail: {mail_pass}"""

    if second_mail.strip():
        result += f"\n2nd mail: {second_mail}"

    result += f"\ncookie: {cookie_result}"

    return result


async def split_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Vui lòng nhập chuỗi sau /split")
        return

    text = " ".join(context.args)
    await update.message.reply_text(format_account(text))


app = ApplicationBuilder().token(TOKEN).build()

# ✅ Chỉ có lệnh /split
app.add_handler(CommandHandler("split", split_command))

app.run_polling()
