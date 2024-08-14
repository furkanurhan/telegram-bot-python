import os
import sys
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# Bot tokeni
TOKEN = os.environ.get('TOKEN')

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Start komutunu yönetir."""
    logger.debug("Start komutu çalıştırıldı.")
    update.message.reply_text('Başlatıldı.')

def add_button(update: Update, context: CallbackContext) -> None:
    """Buton ekleyen fonksiyon."""
    try:
        logger.debug("add_button fonksiyonu çalıştırıldı.")
        keyboard = [
            [InlineKeyboardButton("🔗 FORUM GİRİŞ", url="https://www.kazananlarklubu.com")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Buton ve mesaj
        context.bot.send_message(chat_id=update.effective_chat.id, text="Daha Fazla Bilgi İçin ⬇️", reply_markup=reply_markup)

        logger.info("Buton başarıyla gönderildi.")
    except Exception as e:
        logger.error(f"Buton gönderilirken hata oluştu: {e}")
        update.message.reply_text(f"Buton gönderilirken hata oluştu: {e}")

def update_bot(update: Update, context: CallbackContext) -> None:
    """Botu yeniden başlatmak için kullanılan komut."""
    logger.info("Update komutu çalıştırıldı.")
    update.message.reply_text('Güncellendi.')
    
    # Python betiğini sistem komutuyla yeniden başlatır
    subprocess.call([sys.executable, os.path.abspath(__file__)])

    # Botu durdurur
    os._exit(0)

def main():
    """Botun ana fonksiyonu."""
    logger.info("Bot başlatılıyor.")
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Komut ve mesaj yöneticileri eklenir
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("update", update_bot))  # Update komutu eklendi
    dispatcher.add_handler(MessageHandler(Filters.text | Filters.forwarded, add_button))

    # Botu başlatır
    updater.start_polling()

    # Botu sonsuz döngüde çalışır halde tutar
    updater.idle()

if __name__ == '__main__':
    main()

