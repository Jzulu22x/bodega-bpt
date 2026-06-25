import os
import csv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

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

def start(update, context):
    update.message.reply_text("BodegaBot activo. Enviame la referencia. Ejemplo: GM-566")

def buscar(update, context):
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
    update.message.reply_text(respuesta)

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, buscar))
updater.start_polling()
updater.idle()
