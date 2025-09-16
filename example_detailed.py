#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пример использования полнофункционального парсера с подробной информацией
"""

from wb_parser import WBParser
from mayak_api import MayakAPI


def example_basic_search():
    """Пример базового поиска без подробной информации"""
    print("🔍 Пример 1: Базовый поиск")
    print("-" * 40)
    
    parser = WBParser()
    
    query = "телефон"
    product_ids = parser.search_products(query)
    
    print(f"Запрос: '{query}'")
    print(f"Найдено ID: {len(product_ids)}")
    print(f"Первые 5 ID: {product_ids[:5]}")
    print()


def example_with_cookies_demo():
    """Пример демонстрации структуры с cookies (без реального запроса)"""
    print("🔍 Пример 2: Структура работы с подробной информацией")
    print("-" * 40)
    
    # Пример cookies (замените на реальные для работы)
    demo_cookies = "session_id=demo; user_token=demo_token"
    
    print("Шаги для получения подробной информации:")
    print("1. Создаем парсер с cookies:")
    print(f"   parser = WBParser(mayak_cookies='{demo_cookies[:30]}...')")
    print()
    
    print("2. Выполняем поиск с подробной информацией:")
    print("   result = parser.search_and_get_detailed_info('iPhone', max_products=10)")
    print()
    
    print("3. Структура результата:")
    demo_result = {
        'query': 'iPhone',
        'page': 1,
        'found_ids': [123456, 789012, 345678],
        'detailed_info': [
            {
                'id': 123456,
                'name': 'iPhone 15 Pro',
                'price': 89999,
                'rating': 4.8,
                'reviews': 1250
            },
            # ... другие товары
        ],
        'total_found': 3,
        'total_detailed': 3
    }
    
    import json
    print(json.dumps(demo_result, ensure_ascii=False, indent=2))
    print()


def example_mayak_api_structure():
    """Пример структуры работы с Mayak API"""
    print("🔍 Пример 3: Прямая работа с Mayak API")
    print("-" * 40)
    
    print("Создание клиента Mayak API:")
    print("api = MayakAPI(cookies='ваши_cookies_здесь')")
    print()
    
    print("Получение информации о товарах:")
    print("product_ids = [306897066, 164105063, 244733060]")
    print("detailed_info = api.get_all_products_info(product_ids)")
    print()
    
    print("Автоматическое разбиение на чанки по 20:")
    large_list = list(range(1, 51))
    api = MayakAPI()  # Без cookies для демо
    chunks = api.split_codes_to_chunks(large_list)
    
    print(f"Исходный список: {len(large_list)} элементов")
    print(f"Разбито на {len(chunks)} чанков:")
    for i, chunk in enumerate(chunks, 1):
        print(f"  Чанк {i}: {len(chunk)} элементов")
    print()


def example_cli_commands():
    """Примеры CLI команд"""
    print("🔍 Пример 4: CLI команды")
    print("-" * 40)
    
    commands = [
        "# Базовый поиск ID",
        "python3 wb_full_cli.py -q 'куртка женская черная'",
        "",
        "# Поиск с подробной информацией",
        "python3 wb_full_cli.py -q 'iPhone' --detailed --cookies-file cookies.txt",
        "",
        "# Подробная информация для конкретных ID", 
        "python3 wb_full_cli.py --ids '306897066,164105063,244733060' --detailed --cookies 'session=...'",
        "",
        "# Сохранение результатов",
        "python3 wb_full_cli.py -q 'телефон' --detailed --save results.json --cookies-file cookies.txt",
        "",
        "# Ограничение количества товаров",
        "python3 wb_full_cli.py -q 'ноутбук' --detailed --max-products 10 --cookies-file cookies.txt"
    ]
    
    for cmd in commands:
        print(cmd)
    print()


def main():
    """Основная функция с примерами"""
    print("📚 Примеры использования WB Full Parser")
    print("=" * 60)
    print()
    
    example_basic_search()
    example_with_cookies_demo()
    example_mayak_api_structure()
    example_cli_commands()
    
    print("💡 Важные замечания:")
    print("- Для получения подробной информации нужны действующие cookies от mayak.bz")
    print("- Cookies можно получить из браузера после авторизации на mayak.bz")
    print("- Максимум 20 товаров за один запрос к Mayak API")
    print("- Большие списки автоматически разбиваются на чанки")


if __name__ == "__main__":
    main()
