#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Полная демонстрация возможностей WB Parser
"""

from wb_parser import WBParser
from mayak_api import MayakAPI
import json


def demo_basic_search():
    """Демо базового поиска"""
    print("🎯 ДЕМО 1: Базовый поиск товаров")
    print("=" * 50)
    
    parser = WBParser()
    
    # Поиск по запросу
    query = "куртка женская черная"
    print(f"Поиск по запросу: '{query}'")
    
    product_ids = parser.search_products(query)
    total = parser.get_total_products(query)
    
    print(f"✅ Найдено {len(product_ids)} ID на первой странице")
    print(f"📊 Всего товаров в каталоге: {total}")
    print(f"🔢 Первые 10 ID: {product_ids[:10]}")
    print()


def demo_multiple_pages():
    """Демо поиска по нескольким страницам"""
    print("🎯 ДЕМО 2: Поиск по нескольким страницам")
    print("=" * 50)
    
    parser = WBParser()
    query = "iPhone"
    pages = 2
    
    print(f"Поиск по запросу: '{query}' на {pages} страницах")
    
    all_ids = []
    for page in range(1, pages + 1):
        print(f"📄 Загрузка страницы {page}...")
        page_ids = parser.search_products(query, page)
        all_ids.extend(page_ids)
        print(f"   Найдено: {len(page_ids)} товаров")
    
    print(f"✅ Всего собрано {len(all_ids)} уникальных ID")
    print(f"🔢 Уникальных ID: {len(set(all_ids))}")
    print()


def demo_mayak_api_structure():
    """Демо структуры работы с Mayak API"""
    print("🎯 ДЕМО 3: Структура работы с Mayak API")
    print("=" * 50)
    
    # Демо без реального запроса
    print("🔧 Инициализация Mayak API:")
    demo_cookies = "session_id=demo; user_token=demo_value"
    api = MayakAPI(demo_cookies)
    print(f"   Cookies установлены: {len(api.session.cookies)} штук")
    
    print("\n📦 Разбиение больших списков на чанки:")
    large_list = list(range(1, 55))  # 54 элемента
    chunks = api.split_codes_to_chunks(large_list)
    print(f"   Исходный список: {len(large_list)} элементов")
    print(f"   Разбито на {len(chunks)} чанков:")
    for i, chunk in enumerate(chunks, 1):
        print(f"     Чанк {i}: {len(chunk)} элементов")
    
    print("\n🌐 Структура запроса к API:")
    print(f"   URL: {api.BASE_URL}{api.PRODUCTS_ENDPOINT}")
    print(f"   Максимум кодов за запрос: {api.MAX_CODES_PER_REQUEST}")
    print()


def demo_cli_examples():
    """Демо CLI команд"""
    print("🎯 ДЕМО 4: Примеры CLI команд")
    print("=" * 50)
    
    examples = [
        {
            "title": "Базовый поиск",
            "command": 'python3 wb_cli.py -q "куртка женская черная"',
            "description": "Получение списка ID товаров"
        },
        {
            "title": "Поиск с общим количеством",
            "command": 'python3 wb_cli.py -q "iPhone" --total',
            "description": "Показ общего количества найденных товаров"
        },
        {
            "title": "JSON формат с сохранением",
            "command": 'python3 wb_cli.py -q "телефон" --format json --save',
            "description": "Сохранение результатов в JSON файл"
        },
        {
            "title": "Полнофункциональный поиск с подробной информацией",
            "command": 'python3 wb_full_cli.py -q "ноутбук" --detailed --cookies-file cookies.txt',
            "description": "Получение подробной информации о товарах"
        },
        {
            "title": "Работа с конкретными ID",
            "command": 'python3 wb_full_cli.py --ids "306897066,164105063" --detailed --cookies-file cookies.txt',
            "description": "Подробная информация для конкретных товаров"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['title']}")
        print(f"   Команда: {example['command']}")
        print(f"   Описание: {example['description']}")
        print()


def demo_integration_example():
    """Демо интеграции в собственный код"""
    print("🎯 ДЕМО 5: Интеграция в собственный код")
    print("=" * 50)
    
    print("💻 Пример кода для интеграции:")
    code_example = '''
# Базовое использование
from wb_parser import WBParser

parser = WBParser()
product_ids = parser.search_products("iPhone")

# С подробной информацией (требуются cookies)
cookies = "ваши_cookies_от_mayak_bz"
parser_detailed = WBParser(mayak_cookies=cookies)
result = parser_detailed.search_and_get_detailed_info("iPhone", max_products=10)

# Обработка результатов
print(f"Найдено товаров: {len(result['found_ids'])}")
print(f"Подробная информация: {len(result['detailed_info'])} товаров")

for item in result['detailed_info']:
    print(f"- {item.get('name', 'N/A')}: {item.get('price', 'N/A')} руб.")
'''
    
    print(code_example)
    print()


def demo_file_formats():
    """Демо различных форматов файлов"""
    print("🎯 ДЕМО 6: Форматы сохранения данных")
    print("=" * 50)
    
    # Демо данные
    demo_data = {
        "query": "демо товар",
        "found_ids": [123456, 789012, 345678],
        "total_found": 3
    }
    
    formats = [
        {
            "name": "JSON",
            "extension": ".json",
            "description": "Структурированный формат для программной обработки"
        },
        {
            "name": "CSV", 
            "extension": ".csv",
            "description": "Табличный формат для Excel и других таблиц"
        },
        {
            "name": "TXT",
            "extension": ".txt", 
            "description": "Простой текстовый список для ручного просмотра"
        }
    ]
    
    print("📁 Поддерживаемые форматы:")
    for fmt in formats:
        print(f"   {fmt['name']} ({fmt['extension']}): {fmt['description']}")
    
    print(f"\n📄 Пример JSON структуры:")
    print(json.dumps(demo_data, ensure_ascii=False, indent=2))
    print()


def main():
    """Главная демонстрация"""
    print("🚀 ПОЛНАЯ ДЕМОНСТРАЦИЯ WB PARSER")
    print("=" * 60)
    print("Демонстрация всех возможностей парсера WildBerries")
    print("=" * 60)
    print()
    
    # Запускаем все демо
    demo_basic_search()
    demo_multiple_pages()
    demo_mayak_api_structure()
    demo_cli_examples()
    demo_integration_example()
    demo_file_formats()
    
    print("🎉 ЗАКЛЮЧЕНИЕ")
    print("=" * 50)
    print("✅ Базовая функциональность: поиск и получение ID товаров")
    print("✅ Расширенная функциональность: подробная информация через Mayak API")
    print("✅ Множественные интерфейсы: CLI, интерактивный режим, API")
    print("✅ Различные форматы вывода: JSON, CSV, TXT")
    print("✅ Автоматическое управление запросами и ошибками")
    print()
    print("💡 Для получения подробной информации о товарах:")
    print("   1. Получите cookies от https://app.mayak.bz")
    print("   2. Используйте wb_full_cli.py с параметром --detailed")
    print("   3. Или интегрируйте WBParser с mayak_cookies в свой код")
    print()
    print("📚 Документация: README.md")
    print("🧪 Тестирование: python3 test_*.py")


if __name__ == "__main__":
    main()
