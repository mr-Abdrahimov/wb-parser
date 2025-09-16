#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WildBerries Full CLI Parser
Полнофункциональный CLI парсер с поддержкой Mayak API для получения подробной информации
"""

import argparse
import sys
import json
import os
from wb_parser import WBParser
from mayak_api import MayakAPI, parse_cookies_string


def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='WildBerries Full Parser - поиск товаров и получение подробной информации',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:
  # Только поиск ID
  %(prog)s -q "куртка женская черная"
  
  # Поиск с подробной информацией
  %(prog)s -q "iPhone" --detailed --cookies "cookie1=value1; cookie2=value2"
  
  # Подробная информация для конкретных ID
  %(prog)s --ids 123456,789012 --detailed --cookies-file cookies.txt
  
  # Сохранение подробной информации
  %(prog)s -q "телефон" --detailed --save results.json --cookies-file cookies.txt
        '''
    )
    
    # Основные параметры поиска
    search_group = parser.add_argument_group('Параметры поиска')
    search_group.add_argument(
        '-q', '--query',
        type=str,
        help='Поисковый запрос'
    )
    
    search_group.add_argument(
        '--ids',
        type=str,
        help='Список ID товаров через запятую (альтернатива поиску)'
    )
    
    search_group.add_argument(
        '-p', '--page',
        type=int,
        default=1,
        help='Номер страницы (по умолчанию: 1)'
    )
    
    search_group.add_argument(
        '--pages',
        type=int,
        help='Количество страниц для загрузки'
    )
    
    # Параметры для подробной информации
    detail_group = parser.add_argument_group('Подробная информация')
    detail_group.add_argument(
        '--detailed',
        action='store_true',
        help='Получить подробную информацию о товарах через Mayak API'
    )
    
    detail_group.add_argument(
        '--cookies',
        type=str,
        help='Cookies для Mayak API в виде строки'
    )
    
    detail_group.add_argument(
        '--cookies-file',
        type=str,
        help='Файл с cookies для Mayak API'
    )
    
    detail_group.add_argument(
        '--max-products',
        type=int,
        default=20,
        help='Максимальное количество товаров для подробной информации (по умолчанию: 20)'
    )
    
    detail_group.add_argument(
        '--sort-by-sales',
        action='store_true',
        help='Сортировать товары по продажам (от большего к меньшему)'
    )
    
    detail_group.add_argument(
        '--show-table',
        action='store_true', 
        help='Показать товары в виде таблицы с продажами'
    )
    
    # Параметры вывода
    output_group = parser.add_argument_group('Параметры вывода')
    output_group.add_argument(
        '-s', '--save',
        type=str,
        nargs='?',
        const='auto',
        help='Сохранить результаты в файл'
    )
    
    output_group.add_argument(
        '--format',
        choices=['list', 'json', 'csv'],
        default='json',
        help='Формат вывода (по умолчанию: json)'
    )
    
    output_group.add_argument(
        '--quiet',
        action='store_true',
        help='Тихий режим'
    )
    
    output_group.add_argument(
        '--total',
        action='store_true',
        help='Показать общее количество найденных товаров'
    )
    
    return parser.parse_args()


def load_cookies_from_file(filepath: str) -> str:
    """Загружает cookies из файла"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"❌ Ошибка при чтении файла cookies: {e}")
        return ""


def format_output(data, format_type='json'):
    """Форматирование вывода"""
    if format_type == 'json':
        return json.dumps(data, ensure_ascii=False, indent=2)
    elif format_type == 'csv':
        # Для CSV нужна более сложная логика в зависимости от структуры данных
        return json.dumps(data, ensure_ascii=False, indent=2)  # Пока JSON
    else:  # list
        if isinstance(data, dict):
            if 'found_ids' in data:
                lines = [f"Запрос: {data.get('query', 'N/A')}"]
                lines.append(f"Найдено ID: {len(data['found_ids'])}")
                if data.get('detailed_info'):
                    lines.append(f"Подробная информация: {len(data['detailed_info'])} товаров")
                lines.append("ID товаров:")
                for i, product_id in enumerate(data['found_ids'], 1):
                    lines.append(f"{i:3d}. {product_id}")
                return '\n'.join(lines)
            elif isinstance(data, list):
                return '\n'.join(str(item) for item in data)
        return str(data)


def save_results(data, filename, format_type='json'):
    """Сохранение результатов в файл"""
    try:
        if filename == 'auto':
            # Автоматическое имя файла
            if isinstance(data, dict) and 'query' in data:
                safe_query = data['query'].replace(' ', '_').replace('/', '_')
                filename = f"wb_full_{safe_query}.{format_type if format_type != 'list' else 'txt'}"
            else:
                filename = f"wb_full_results.{format_type if format_type != 'list' else 'txt'}"
        
        content = format_output(data, format_type)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Результаты сохранены в файл: {filename}")
        return True
    except Exception as e:
        print(f"❌ Ошибка при сохранении: {e}")
        return False


def main():
    """Основная функция CLI"""
    args = parse_arguments()
    
    # Проверяем обязательные параметры
    if not args.query and not args.ids:
        print("❌ Необходимо указать либо --query для поиска, либо --ids для конкретных товаров")
        sys.exit(1)
    
    # Получаем cookies если нужна подробная информация
    cookies = None
    if args.detailed:
        if args.cookies:
            cookies = args.cookies
        elif args.cookies_file:
            cookies = load_cookies_from_file(args.cookies_file)
        
        if not cookies:
            print("❌ Для получения подробной информации необходимо указать cookies через --cookies или --cookies-file")
            sys.exit(1)
    
    # Настройка логирования
    if args.quiet:
        import logging
        logging.getLogger().setLevel(logging.ERROR)
    
    try:
        # Создаем парсер
        parser = WBParser(mayak_cookies=cookies if args.detailed else None)
        
        if args.ids:
            # Работаем с конкретными ID
            ids_list = [int(id_str.strip()) for id_str in args.ids.split(',')]
            
            if not args.quiet:
                print(f"🔍 Получение информации для {len(ids_list)} товаров")
            
            if args.detailed:
                detailed_info = parser.get_products_detailed_info(ids_list)
                result = {
                    'mode': 'ids',
                    'ids': ids_list,
                    'detailed_info': detailed_info,
                    'total_detailed': len(detailed_info)
                }
            else:
                result = {
                    'mode': 'ids',
                    'ids': ids_list,
                    'total': len(ids_list)
                }
        
        else:
            # Поиск по запросу
            if not args.quiet:
                print(f"🔍 Поиск по запросу: '{args.query}'")
            
            # Показываем общее количество если запрошено
            if args.total and not args.quiet:
                total = parser.get_total_products(args.query)
                print(f"📊 Всего найдено товаров: {total}")
            
            if args.detailed:
                # Получаем подробную информацию
                result = parser.search_and_get_detailed_info(
                    args.query, 
                    args.page, 
                    args.max_products
                )
            else:
                # Только ID
                if args.pages:
                    # Несколько страниц
                    all_ids = []
                    for page in range(1, args.pages + 1):
                        if not args.quiet:
                            print(f"📄 Загружается страница {page}...")
                        page_ids = parser.search_products(args.query, page)
                        if not page_ids:
                            break
                        all_ids.extend(page_ids)
                    
                    result = {
                        'query': args.query,
                        'pages': args.pages,
                        'found_ids': all_ids,
                        'total_found': len(all_ids)
                    }
                else:
                    # Одна страница
                    product_ids = parser.search_products(args.query, args.page)
                    result = {
                        'query': args.query,
                        'page': args.page,
                        'found_ids': product_ids,
                        'total_found': len(product_ids)
                    }
        
        # Выводим результаты
        if result:
            if not args.quiet:
                if 'total_found' in result:
                    print(f"📦 Найдено товаров: {result['total_found']}")
                if 'total_detailed' in result:
                    print(f"📋 Подробная информация: {result['total_detailed']} товаров")
                
                if not args.detailed or args.format != 'json':
                    print("\n" + "="*60)
            
            # Показываем таблицу с продажами если запрошено
            if args.show_table and result.get('detailed_info'):
                if not args.quiet:
                    print("\n" + parser.display_products_by_sales(result['detailed_info']))
                    print()
            
            # Форматируем и выводим
            if args.quiet and args.format == 'json':
                print(format_output(result, args.format))
            elif not args.quiet:
                if not args.show_table:  # Если таблица уже показана, не дублируем
                    print(format_output(result, args.format))
                    print("="*60)
            
            # Сохраняем если нужно
            if args.save:
                save_results(result, args.save, args.format)
        
        else:
            if not args.quiet:
                print("❌ Результаты не получены")
            sys.exit(1)
    
    except Exception as e:
        if not args.quiet:
            print(f"❌ Произошла ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Программа прервана пользователем")
        sys.exit(0)
