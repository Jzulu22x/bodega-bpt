import os
import csv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")
CSV_PATH = "referencias.csv"

def cargar():
    datos = {}
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ref = list(row.values())[0].strip().upper()
            zona = list(row.values())[1].strip() if list(row.values())[1] else ''
            datos[ref] = zona
    return datos

datos = cargar()

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *BodegaBot activo*\n\nEnvíame la referencia y te digo dónde está.\n\nE
