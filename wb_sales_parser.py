#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WB Sales Parser - простой парсер для получения ID, pics отсортированных по продажам
"""

import argparse
import logging
import sys
import csv
from typing import List, Dict, Any
from wb_parser import WBParser
from mayak_api import parse_cookies_string

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def write_csv(path: str, products: List[Dict[str, Any]]):
    """Сохраняет CSV со столбцами: Ссылка, Название, Количество продаж, Изображения"""
    fieldnames = ["Ссылка", "Название", "Количество продаж", "Изображения"]
    
    try:
        with open(path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for p in products:
                product_id = p.get('id', '')
                url = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx" if product_id else ''
                name = p.get('name', '')
                sales = p.get('sales', 0)
                image_urls = p.get('image_urls', [])
                images_joined = '\n'.join(image_urls) if image_urls else ''
                writer.writerow({
                    "Ссылка": url,
                    "Название": name,
                    "Количество продаж": sales,
                    "Изображения": images_joined,
                })
        logger.info(f"CSV сохранён: {path}")
    except Exception as e:
        logger.error(f"Ошибка записи CSV: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Получение списка товаров WB отсортированных по продажам',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        '-q', '--query',
        type=str,
        required=True,
        help='Поисковый запрос'
    )
    parser.add_argument(
        '--cookies-file',
        type=str,
        default='cookies.txt',
        help='Файл с cookies для Mayak API (по умолчанию: cookies.txt)'
    )
    parser.add_argument(
        '--max-products',
        type=int,
        default=20,
        help='Максимальное количество товаров (по умолчанию: 20)'
    )
    
    parser.add_argument(
        '--show-table',
        action='store_true',
        help='Показать результаты в виде таблицы'
    )
    
    parser.add_argument(
        '--show-images',
        action='store_true',
        help='Показать ссылки на изображения'
    )
    
    parser.add_argument(
        '--images-only',
        action='store_true',
        help='Показать только ссылки на изображения (по одной на строку)'
    )
    
    parser.add_argument(
        '--csv',
        type=str,
        help='Сохранить результат в CSV файл (столбцы: Ссылка, Название, Количество продаж, Изображения)'
    )
    
    args = parser.parse_args()
    
    # Загружаем cookies
    mayak_cookies = None
    try:
        with open(args.cookies_file, 'r') as f:
            mayak_cookies = f.read().strip()
        if not mayak_cookies:
            logger.error("Файл с cookies пуст.")
            sys.exit(1)
    except FileNotFoundError:
        logger.error(f"Файл с cookies не найден: {args.cookies_file}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Ошибка при чтении файла cookies: {e}")
        sys.exit(1)
    
    # Инициализируем парсер с cookies
    wb_parser = WBParser(mayak_cookies=mayak_cookies)
    
    logger.info(f"Начинаем поиск и получение подробной информации для запроса: '{args.query}'")
    
    # Получаем подробную информацию с pics и сортировкой
    combined_products = wb_parser.get_products_detailed_info_with_pics(
        args.query, 
        page=1, 
        max_products=args.max_products
    )
    
    if not combined_products:
        logger.warning("Не удалось получить подробную информацию о товарах.")
        sys.exit(1)
    
    # Экспорт CSV при необходимости
    if args.csv:
        write_csv(args.csv, combined_products)
        print(f"✅ CSV сохранён: {args.csv}")
        return
    
    # Иначе, обычный вывод
    if args.images_only:
        print("\n🖼️ Ссылки на изображения:")
        for product in combined_products:
            image_urls = product.get('image_urls', [])
            for url in image_urls:
                print(url)
    elif args.show_table:
        print("\n" + wb_parser.display_products_by_sales(combined_products))
        if args.show_images:
            print("\n🖼️ Ссылки на изображения:")
            for product in combined_products:
                product_id = product.get('id', 'N/A')
                image_urls = product.get('image_urls', [])
                if image_urls:
                    print(f"\nТовар {product_id} ({len(image_urls)} изображений):")
                    for i, url in enumerate(image_urls, 1):
                        print(f"  {i}. {url}")
    else:
        print("\n📋 Список товаров (отсортированы по продажам):")
        print("ID товара | Продажи | Фото")
        print("-" * 30)
        for product in combined_products:
            product_id = product.get('id', 'N/A')
            sales = product.get('sales', 0)
            pics = product.get('pics', 0)
            print(f"{product_id} | {sales:,} | {pics}")
        if args.show_images:
            print("\n🖼️ Ссылки на изображения:")
            for product in combined_products:
                product_id = product.get('id', 'N/A')
                image_urls = product.get('image_urls', [])
                if image_urls:
                    print(f"\nТовар {product_id} ({len(image_urls)} изображений):")
                    for i, url in enumerate(image_urls, 1):
                        print(f"  {i}. {url}")

if __name__ == "__main__":
    main()

