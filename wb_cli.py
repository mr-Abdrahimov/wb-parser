#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WildBerries CLI Parser
Парсер с поддержкой аргументов командной строки
"""

import argparse
import sys
from wb_parser import WBParser


def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='WildBerries Parser - парсинг товаров с WB',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:
  %(prog)s -q "куртка женская черная"
  %(prog)s --query "iPhone" --page 2
  %(prog)s -q "телефон Samsung" --save
  %(prog)s -q "кроссовки Nike" -p 1 -s results.txt
  %(prog)s --query "ноутбук" --pages 3 --save
        '''
    )
    
    parser.add_argument(
        '-q', '--query',
        type=str,
        required=True,
        help='Поисковый запрос (обязательный параметр)'
    )
    
    parser.add_argument(
        '-p', '--page',
        type=int,
        default=1,
        help='Номер страницы (по умолчанию: 1)'
    )
    
    parser.add_argument(
        '--pages',
        type=int,
        help='Количество страниц для загрузки (загружает с 1 по указанную страницу)'
    )
    
    parser.add_argument(
        '-s', '--save',
        type=str,
        nargs='?',
        const='auto',
        help='Сохранить результаты в файл. Можно указать имя файла или использовать автоматическое имя'
    )
    
    parser.add_argument(
        '--total',
        action='store_true',
        help='Показать общее количество найденных товаров'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Тихий режим - только результаты, без логов'
    )
    
    parser.add_argument(
        '--format',
        choices=['list', 'json', 'csv'],
        default='list',
        help='Формат вывода результатов (по умолчанию: list)'
    )
    
    return parser.parse_args()


def format_output(product_ids, query, format_type='list'):
    """Форматирование вывода результатов"""
    if format_type == 'json':
        import json
        result = {
            'query': query,
            'count': len(product_ids),
            'product_ids': product_ids
        }
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    elif format_type == 'csv':
        lines = ['query,product_id']
        for product_id in product_ids:
            lines.append(f'"{query}",{product_id}')
        return '\n'.join(lines)
    
    else:  # list format
        lines = [f"Запрос: {query}"]
        lines.append(f"Найдено: {len(product_ids)} товаров")
        lines.append("ID товаров:")
        for i, product_id in enumerate(product_ids, 1):
            lines.append(f"{i:3d}. {product_id}")
        return '\n'.join(lines)


def save_results(product_ids, query, filename, format_type='list'):
    """Сохранение результатов в файл"""
    if filename == 'auto':
        # Автоматическое имя файла
        safe_query = query.replace(' ', '_').replace('/', '_').replace('\\', '_')
        if format_type == 'json':
            filename = f"wb_{safe_query}.json"
        elif format_type == 'csv':
            filename = f"wb_{safe_query}.csv"
        else:
            filename = f"wb_{safe_query}.txt"
    
    try:
        content = format_output(product_ids, query, format_type)
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
    
    # Настройка логирования в зависимости от quiet режима
    if args.quiet:
        import logging
        logging.getLogger().setLevel(logging.ERROR)
    
    # Создаем парсер
    wb_parser = WBParser()
    
    if not args.quiet:
        print(f"🔍 Поиск по запросу: '{args.query}'")
    
    # Показываем общее количество товаров, если запрошено
    if args.total and not args.quiet:
        total = wb_parser.get_total_products(args.query)
        print(f"📊 Всего найдено товаров: {total}")
    
    all_product_ids = []
    
    # Определяем количество страниц для загрузки
    if args.pages:
        pages_to_load = list(range(1, args.pages + 1))
        if not args.quiet:
            print(f"📄 Загружаем {args.pages} страниц...")
    else:
        pages_to_load = [args.page]
        if args.page != 1 and not args.quiet:
            print(f"📄 Загружаем страницу {args.page}...")
    
    # Загружаем данные
    for page_num in pages_to_load:
        if not args.quiet and len(pages_to_load) > 1:
            print(f"⏳ Загружается страница {page_num}...")
        
        product_ids = wb_parser.search_products(args.query, page_num)
        
        if not product_ids:
            if not args.quiet:
                print(f"⚠️  На странице {page_num} товары не найдены")
            break
        
        all_product_ids.extend(product_ids)
        
        if not args.quiet and len(pages_to_load) > 1:
            print(f"✅ Страница {page_num}: найдено {len(product_ids)} товаров")
    
    # Выводим результаты
    if all_product_ids:
        if not args.quiet:
            print(f"\n📦 Всего получено {len(all_product_ids)} ID товаров")
            # Показываем результаты в выбранном формате
            output = format_output(all_product_ids, args.query, args.format)
            print("\n" + "="*60)
            print(output)
            print("="*60)
        
        # Сохраняем, если запрошено
        if args.save:
            save_results(all_product_ids, args.query, args.save, args.format)
        
        # В тихом режиме выводим только результаты
        if args.quiet:
            if args.format == 'json':
                print(format_output(all_product_ids, args.query, 'json'))
            elif args.format == 'csv':
                print(format_output(all_product_ids, args.query, 'csv'))
            else:
                for product_id in all_product_ids:
                    print(product_id)
    
    else:
        if not args.quiet:
            print("❌ Товары не найдены")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Программа прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
        sys.exit(1)
