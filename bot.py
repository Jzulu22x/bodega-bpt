import os
import csv
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")
CSV_PATH = "referencias.csv"

def cargar():
    datos = {}
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            vals = list(row.values())
            ref = vals[0].strip().upper()
            zona = vals[1].strip() if len(vals) > 1 and vals[1] else ''
            datos[ref] = zona
    return datos

datos = cargar()

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("BodegaBot activo. Enviame la referencia. Ejemplo: GM-566")

async def buscar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ref = update.message.text.strip().upper()
    if ref in datos:
        zona = datos[ref]
        if not zona:
            respuesta = f"Producto: {ref}\nSin ubicacion asignada."
        else:
            partes = zona.split("-Z")
            bodega = partes[0] if len(partes) > 1 else zona
            nzona = partes[1] if len(partes) > 1 else zona
            respuesta = f"Producto: {ref}\nBodega: {bodega}\nZona: {nzona}"
    else:
        respuesta = f"Referencia {ref} no encontrada."
    await update.message.reply_text(respuesta)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar))
app.run_polling()
