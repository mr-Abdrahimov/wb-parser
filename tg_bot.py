#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram бот для получения CSV по запросу query.

Команды:
- /start, /help — инструкции
- Любой текст — трактуется как query для поиска на WB, бот вернёт CSV-файл

Требования:
- python-telegram-bot >= 21.4
- Файл cookies.txt в корне проекта (по умолчанию)
"""

import io
import logging
import os
from datetime import datetime
from typing import List, Dict, Any

from telegram import Update, InputFile
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from wb_parser import WBParser

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
COOKIES_FILE = os.getenv('COOKIES_FILE', 'cookies.txt')


def products_to_csv_bytes(products: List[Dict[str, Any]]) -> bytes:
    """Готовит CSV в памяти с колонками: Ссылка, Название, Количество продаж, Изображения"""
    import csv

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Ссылка", "Название", "Количество продаж", "Изображения"])

    for p in products:
        product_id = p.get('id', '')
        url = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx" if product_id else ''
        name = p.get('name', '')
        sales = p.get('sales', 0)
        images = p.get('image_urls', []) or []
        images_joined = "\n".join(images)
        writer.writerow([url, name, sales, images_joined])

    data = output.getvalue().encode('utf-8-sig')
    output.close()
    return data


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "Привет! Пришлите текст запроса (query), например:\n"
        "куртка женская черная\n\n"
        "Я выполню парсинг и пришлю .csv файл с колонками: \n"
        "Ссылка, Название, Количество продаж, Изображения."
    )
    await update.message.reply_text(text)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = (update.message.text or '').strip()
    if not query:
        await update.message.reply_text("Пустой запрос. Пришлите текст запроса.")
        return

    # Уведомление о загрузке
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_DOCUMENT)

    # Читаем cookies
    try:
        with open(COOKIES_FILE, 'r') as f:
            mayak_cookies = f.read().strip()
        if not mayak_cookies:
            await update.message.reply_text("Файл cookies пуст. Заполните cookies.txt")
            return
    except FileNotFoundError:
        await update.message.reply_text("Файл cookies.txt не найден в корне проекта")
        return
    except Exception as e:
        logger.exception("Ошибка чтения cookies")
        await update.message.reply_text(f"Ошибка чтения cookies: {e}")
        return

    try:
        parser = WBParser(mayak_cookies=mayak_cookies)
        products = parser.get_products_detailed_info_with_pics(query=query, page=1, max_products=20)
        if not products:
            await update.message.reply_text("Ничего не найдено или ошибка при получении данных.")
            return

        csv_bytes = products_to_csv_bytes(products)
        filename = f"wb_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        await update.message.reply_document(document=InputFile(io.BytesIO(csv_bytes), filename=filename),
                                            caption=f"Результат для запроса: {query}")
    except Exception as e:
        logger.exception("Ошибка в обработке запроса")
        await update.message.reply_text(f"Ошибка: {e}")


def build_app() -> Application:
    token = TELEGRAM_BOT_TOKEN or ""
    return Application.builder().token(token).build()


def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Не задан TELEGRAM_BOT_TOKEN (экспортируйте переменную окружения)")
        raise SystemExit(1)

    application = build_app()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query))

    logger.info("Telegram бот запущен. Ожидание сообщений...")
    application.run_polling()


if __name__ == "__main__":
    main()
