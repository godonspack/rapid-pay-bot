import os

from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

app = FastAPI()

telegram_app = (
    Application.builder()
    .token(BOT_TOKEN)
    .updater(None)
    .build()
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_text(
        f"👋 Welcome to Rapid Pay, {user.first_name}!\n\n"
        "💰 Watch advertisements and earn rewards.\n"
        "👥 Invite friends and earn referral bonuses.\n\n"
        "🚀 Your Rapid Pay journey starts here!"
    )


telegram_app.add_handler(CommandHandler("start", start))


@app.on_event("startup")
async def startup():
    await telegram_app.initialize()
    await telegram_app.start()

    await telegram_app.bot.set_webhook(
        url=f"{WEBHOOK_URL}/telegram"
    )


@app.on_event("shutdown")
async def shutdown():
    await telegram_app.stop()
    await telegram_app.shutdown()


@app.post("/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)

    await telegram_app.process_update(update)

    return {"ok": True}


@app.get("/")
async def home():
    return {"status": "Rapid Pay is running"}
