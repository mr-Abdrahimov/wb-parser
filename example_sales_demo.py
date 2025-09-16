#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрация работы с данными о продажах от Mayak API
"""

from wb_parser import WBParser
from mayak_api import MayakAPI
import json


def demo_sales_data_processing():
    """Демонстрация обработки данных о продажах"""
    print("🎯 ДЕМО: Обработка данных о продажах от Mayak API")
    print("=" * 60)
    
    # Симулируем реальный ответ от Mayak API
    mock_mayak_response = {
        "306897066": {
            "sales": 12450,
            "revenue": 35678901,
            "lost_revenue": 8765432,
            "avg_price": 2867
        },
        "164105063": {
            "sales": 8765,
            "revenue": 25123456,
            "lost_revenue": 5432198,
            "avg_price": 2867
        },
        "244733060": {
            "sales": 15678,
            "revenue": 45234567,
            "lost_revenue": 12345678,
            "avg_price": 2885
        },
        "64775386": {
            "sales": 7193,
            "revenue": 19747579,
            "lost_revenue": 11161879,
            "avg_price": 2689
        },
        "315813991": {
            "sales": 23456,
            "revenue": 67890123,
            "lost_revenue": 15432167,
            "avg_price": 2894
        }
    }
    
    print("📥 Исходные данные от Mayak API (формат ключ-значение):")
    print(json.dumps(mock_mayak_response, indent=2, ensure_ascii=False))
    print()
    
    # Преобразуем данные как это делает наш API
    products_list = []
    for product_id, product_data in mock_mayak_response.items():
        product_info = product_data.copy()
        product_info['id'] = product_id
        products_list.append(product_info)
    
    print("🔄 После преобразования в список:")
    print(f"Получено {len(products_list)} товаров")
    print("Пример товара:", products_list[0])
    print()
    
    # Сортируем по продажам
    api = MayakAPI()
    sorted_products = api.sort_products_by_sales(products_list, reverse=True)
    
    print("📊 Товары, отсортированные по продажам (убывание):")
    print(api.format_products_table(sorted_products))
    print()
    
    return sorted_products


def demo_integration_with_wb_parser():
    """Демонстрация интеграции с WB Parser"""
    print("🎯 ДЕМО: Интеграция с WB Parser")
    print("=" * 60)
    
    # Создаем парсер (без реальных cookies для демо)
    parser = WBParser()
    
    # Симулируем получение данных
    demo_products = [
        {'id': '315813991', 'sales': 23456, 'revenue': 67890123, 'avg_price': 2894},
        {'id': '244733060', 'sales': 15678, 'revenue': 45234567, 'avg_price': 2885},
        {'id': '306897066', 'sales': 12450, 'revenue': 35678901, 'avg_price': 2867},
        {'id': '164105063', 'sales': 8765, 'revenue': 25123456, 'avg_price': 2867},
        {'id': '64775386', 'sales': 7193, 'revenue': 19747579, 'avg_price': 2689}
    ]
    
    # Создаем временный API для демонстрации
    api = MayakAPI()
    parser.mayak_api = api
    
    print("📋 Отображение через WBParser (топ 3 товара):")
    display_result = parser.display_products_by_sales(demo_products, limit=3)
    print(display_result)
    print()


def demo_cli_commands():
    """Демонстрация CLI команд для работы с продажами"""
    print("🎯 ДЕМО: CLI команды для работы с продажами")
    print("=" * 60)
    
    commands = [
        {
            "title": "Поиск с подробной информацией и таблицей продаж",
            "command": "python3 wb_full_cli.py -q 'iPhone' --detailed --show-table --cookies-file cookies.txt",
            "description": "Получает товары и показывает их в виде таблицы, отсортированной по продажам"
        },
        {
            "title": "Анализ конкретных товаров",
            "command": "python3 wb_full_cli.py --ids '306897066,164105063,244733060' --detailed --show-table --cookies-file cookies.txt",
            "description": "Анализирует продажи конкретных товаров"
        },
        {
            "title": "Топ товаров с ограничением",
            "command": "python3 wb_full_cli.py -q 'куртка женская' --detailed --show-table --max-products 10 --cookies-file cookies.txt",
            "description": "Показывает топ 10 товаров по продажам"
        },
        {
            "title": "Сохранение данных о продажах",
            "command": "python3 wb_full_cli.py -q 'телефон' --detailed --save sales_report.json --cookies-file cookies.txt",
            "description": "Сохраняет полную информацию о продажах в файл"
        }
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"{i}. {cmd['title']}")
        print(f"   Команда: {cmd['command']}")
        print(f"   Описание: {cmd['description']}")
        print()


def demo_data_analysis():
    """Демонстрация анализа данных"""
    print("🎯 ДЕМО: Анализ данных о продажах")
    print("=" * 60)
    
    # Получаем отсортированные данные из первого демо
    products = demo_sales_data_processing()
    
    # Анализируем данные
    total_sales = sum(p.get('sales', 0) for p in products)
    total_revenue = sum(p.get('revenue', 0) for p in products)
    total_lost_revenue = sum(p.get('lost_revenue', 0) for p in products)
    avg_price = sum(p.get('avg_price', 0) for p in products) / len(products) if products else 0
    
    print("📈 АНАЛИЗ ПРОДАЖ")
    print("-" * 40)
    print(f"Общее количество продаж: {total_sales:,}")
    print(f"Общая выручка: {total_revenue:,} руб.")
    print(f"Упущенная выручка: {total_lost_revenue:,} руб.")
    print(f"Средняя цена по всем товарам: {avg_price:,.0f} руб.")
    print()
    
    # Топ товар
    if products:
        top_product = products[0]
        print("🏆 ЛИДЕР ПО ПРОДАЖАМ")
        print("-" * 40)
        print(f"ID товара: {top_product.get('id')}")
        print(f"Продаж: {top_product.get('sales', 0):,}")
        print(f"Выручка: {top_product.get('revenue', 0):,} руб.")
        print(f"Средняя цена: {top_product.get('avg_price', 0):,} руб.")
        print(f"Доля от общих продаж: {top_product.get('sales', 0) / total_sales * 100:.1f}%")
    print()


def demo_real_usage_scenario():
    """Демонстрация реального сценария использования"""
    print("🎯 ДЕМО: Реальный сценарий использования")
    print("=" * 60)
    
    scenario = """
🔍 СЦЕНАРИЙ: Анализ конкурентов в категории "куртки женские"

1. Поиск товаров:
   python3 wb_cli.py -q "куртка женская черная" --quiet > ids.txt

2. Получение подробной информации о топ-20 товарах:
   python3 wb_full_cli.py --ids "$(head -20 ids.txt | tr '\\n' ',')" \\
                          --detailed --show-table --cookies-file cookies.txt

3. Сохранение полного отчета:
   python3 wb_full_cli.py -q "куртка женская" \\
                          --detailed --max-products 50 \\
                          --save market_analysis.json \\
                          --cookies-file cookies.txt

4. Анализ результатов:
   - Определение лидеров по продажам
   - Анализ ценовых сегментов
   - Выявление возможностей для входа на рынок
    """
    
    print(scenario)


def main():
    """Главная демонстрация"""
    print("🚀 ДЕМОНСТРАЦИЯ РАБОТЫ С ДАННЫМИ О ПРОДАЖАХ")
    print("=" * 70)
    print()
    
    demo_sales_data_processing()
    demo_integration_with_wb_parser()
    demo_cli_commands()
    demo_data_analysis()
    demo_real_usage_scenario()
    
    print("🎉 ЗАКЛЮЧЕНИЕ")
    print("=" * 60)
    print("✅ Автоматическое преобразование данных из формата Mayak API")
    print("✅ Сортировка товаров по продажам (от большего к меньшему)")
    print("✅ Красивое табличное отображение результатов")
    print("✅ Интеграция с CLI для удобного использования")
    print("✅ Возможность анализа как поисковых результатов, так и конкретных товаров")
    print()
    print("💡 Для работы с реальными данными:")
    print("   1. Получите действующие cookies от https://app.mayak.bz")
    print("   2. Используйте wb_full_cli.py с параметрами --detailed и --show-table")
    print("   3. Анализируйте результаты для принятия бизнес-решений")


if __name__ == "__main__":
    main()
