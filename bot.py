import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")


def parse_line(line):

    # dạng |
    if "|" in line:
        parts = line.split("|")

        while len(parts) < 7:
            parts.append("")

        user_id, password, twofa, mail, mail_pass, second_mail, cookie_full = parts

    else:
        parts = line.split()

        if len(parts) < 5:
            return None

        user_id = parts[0]
        password = parts[1]
        mail = parts[2]
        mail_pass = parts[3]
        twofa = " ".join(parts[4:])

        second_mail = ""
        cookie_full = ""

    # lấy cookie nếu có
    c_user = re.search(r'c_user=[^;]+;', cookie_full)
    xs = re.search(r'xs=[^;]+;', cookie_full)

    cookie_result = ""
    if c_user and xs:
        cookie_result = f"{c_user.group()}{xs.group()}"

    return {
        "id": user_id,
        "pass": password,
        "2fa": twofa,
        "mail": mail,
        "mail_pass": mail_pass,
        "second_mail": second_mail,
        "cookie": cookie_result
    }


def format_account(data, name):

    title = "help me check new profile"
    if name:
        title += f" {name}"

    result = f"""{title} :
id: {data['id']}
pass: {data['pass']}
2fa: {data['2fa']}
mail: {data['mail']}
pass mail: {data['mail_pass']}"""

    if data["second_mail"]:
        result += f"\n2nd mail: {data['second_mail']}"

    result += f"\ncookie: {data['cookie']}"

    return result


# =========================
# /split
# =========================
async def split_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    lines = text.split("\n")

    first_line = lines[0]
    data_lines = lines[1:]

    parts = first_line.split(maxsplit=1)

    name = None
    if len(parts) > 1:
        name = parts[1]

    results = []

    for line in data_lines:

        parsed = parse_line(line)

        if not parsed:
            continue

        results.append(format_account(parsed, name))

    if not results:
        await update.message.reply_text("Không có dữ liệu hợp lệ.")
        return

    final_text = "\n\n".join(results)

    if len(final_text) > 4000:

        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(final_text)

        await update.message.reply_document(open("result.txt", "rb"))

    else:
        await update.message.reply_text(final_text)


# =========================
# MAIN
# =========================
def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("split", split_command))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()