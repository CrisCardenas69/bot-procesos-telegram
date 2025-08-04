import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Cargar procesos desde archivo JSON
with open("procesos.json", "r", encoding="utf-8") as f:
    PROCESOS = json.load(f)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenido al Bot de Procesos de Restaurante X.\nUsa /procesos para ver los procesos disponibles."
    )

# /procesos
async def procesos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "\n".join([f"🔹 {p}" for p in PROCESOS])
    await update.message.reply_text(
        f"Procesos disponibles:\n{lista}\n\nEscribe el nombre de uno para ver el detalle."
    )

# Cuando el usuario escribe el nombre de un proceso
async def responder_proceso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip().lower()
    if texto in PROCESOS:
        info = PROCESOS[texto]
        await update.message.reply_text(f"📄 {info['titulo']}\n\n{info['descripcion']}")

        archivo = info["archivo"]
        if archivo.endswith(".pdf"):
            await update.message.reply_document(open(archivo, "rb"))
        elif archivo.endswith((".jpg", ".jpeg", ".png")):
            await update.message.reply_photo(open(archivo, "rb"))
    else:
        await update.message.reply_text("❌ Proceso no encontrado. Usa /procesos para ver los disponibles.")

# MAIN
TOKEN = "8035682366:AAEnqsTS137HWJClXmHUYN6sHnvGZJ-fIRY"  # <-- Reemplaza con tu token real de BotFather
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("procesos", procesos))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_proceso))
app.run_polling()
