import os
import csv as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")
CSV_PATH = "referencias.csv"

def cargar():
    df = pd.read_csv(CSV_PATH, dtype=str)
    df.columns = [c.strip().lower() for c in df.columns]
    df["referencia"] = df["referencia"].str.upper().str.strip()
    df["zona"] = df["zona"].fillna("").str.strip()
    return df.set_index("referencia")["zona"].to_dict()

datos = cargar()

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *BodegaBot activo*\n\nEnvíame la referencia y te digo dónde está.\n\nEjemplo: `GM-566`",
        parse_mode="Markdown"
    )

async def buscar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ref = update.message.text.strip().upper()
    if ref in datos:
        zona = datos[ref]
        if not zona:
            respuesta = f"📦 *{ref}*\n⚠️ Sin ubicación asignada aún."
        else:
            partes = zona.split("-Z")
            bodega = partes[0] if len(partes) > 1 else zona
            nzona = partes[1] if len(partes) > 1 else zona
            respuesta = (
                f"✅ *Producto encontrado*\n\n"
                f"📦 Referencia: `{ref}`\n"
                f"🏭 Bodega: *{bodega}*\n"
                f"📍 Zona: *{nzona}*"
            )
    else:
        respuesta = f"❌ Referencia `{ref}` no encontrada.\nVerifica que esté bien escrita."
    await update.message.reply_text(respuesta, parse_mode="Markdown")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar))
print("🤖 BodegaBot corriendo...")
app.run_polling()
