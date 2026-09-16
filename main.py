import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_text(
        f"👋 Welcome to Rapid Pay, {user.first_name}!\n\n"
        "💰 Watch advertisements and earn rewards.\n"
        "👥 Invite friends and earn referral bonuses.\n\n"
        "🚀 Your Rapid Pay journey starts here!"
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Rapid Pay is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
