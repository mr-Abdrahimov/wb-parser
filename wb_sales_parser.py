#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WB Sales Parser - простой парсер для получения ID, pics отсортированных по продажам
"""

import argparse
import sys
from wb_parser import WBParser


def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(
        description='Получение списка товаров WB отсортированных по продажам'
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
        required=True,
        help='Файл с cookies для Mayak API'
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
    
    args = parser.parse_args()
    
    # Загружаем cookies
    try:
        with open(args.cookies_file, 'r', encoding='utf-8') as f:
            cookies = f.read().strip()
    except Exception as e:
        print(f"❌ Ошибка при чтении файла cookies: {e}")
        sys.exit(1)
    
    # Создаем парсер
    wb_parser = WBParser(mayak_cookies=cookies)
    
    print(f"🔍 Поиск по запросу: '{args.query}'")
    
    # Получаем данные
    products = wb_parser.get_products_detailed_info_with_pics(
        args.query, 
        page=1, 
        max_products=args.max_products
    )
    
    if not products:
        print("❌ Товары не найдены")
        sys.exit(1)
    
    print(f"✅ Найдено {len(products)} товаров")
    
    if args.show_table:
        # Показываем таблицу
        table = wb_parser.display_products_by_sales(products)
        print("\n" + table)
    else:
        # Показываем простой список
        print("\n📋 Список товаров (отсортированы по продажам):")
        print("ID товара | Продажи | Фото")
        print("-" * 30)
        
        for i, product in enumerate(products, 1):
            product_id = product.get('id', 'N/A')
            sales = product.get('sales', 0)
            pics = product.get('pics', 0)
            print(f"{product_id} | {sales:,} | {pics}")


if __name__ == "__main__":
    main()

