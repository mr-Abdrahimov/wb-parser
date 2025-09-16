#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест функциональности сортировки по продажам
"""

from mayak_api import MayakAPI
from wb_parser import WBParser
import json


def test_data_transformation():
    """Тест преобразования данных из формата Mayak API"""
    print("🧪 Тест преобразования данных...")
    
    # Симулируем ответ от Mayak API
    mock_response = {
        "64775386": {
            "sales": 7193,
            "revenue": 19747579,
            "lost_revenue": 11161879,
            "avg_price": 2689
        },
        "306897066": {
            "sales": 12450,
            "revenue": 35678901,
            "lost_revenue": 8765432,
            "avg_price": 2867
        },
        "164105063": {
            "sales": 3456,
            "revenue": 9876543,
            "lost_revenue": 2345678,
            "avg_price": 2856
        }
    }
    
    # Преобразуем данные как это делает API
    products_list = []
    for product_id, product_data in mock_response.items():
        product_info = product_data.copy()
        product_info['id'] = product_id
        products_list.append(product_info)
    
    print(f"✅ Преобразовано {len(products_list)} товаров")
    print(f"Пример товара: {products_list[0]}")
    return products_list


def test_sales_sorting():
    """Тест сортировки по продажам"""
    print("\n🧪 Тест сортировки по продажам...")
    
    # Получаем тестовые данные
    products = test_data_transformation()
    
    api = MayakAPI()
    sorted_products = api.sort_products_by_sales(products, reverse=True)
    
    # Проверяем что сортировка работает
    sales_values = [p.get('sales', 0) for p in sorted_products]
    is_sorted = all(sales_values[i] >= sales_values[i+1] for i in range(len(sales_values)-1))
    
    if is_sorted:
        print("✅ Сортировка по продажам работает корректно")
        print("Порядок товаров по продажам:")
        for i, product in enumerate(sorted_products, 1):
            print(f"  {i}. ID {product['id']}: {product['sales']:,} продаж")
        return True
    else:
        print("❌ Сортировка по продажам не работает")
        return False


def test_table_formatting():
    """Тест форматирования таблицы"""
    print("\n🧪 Тест форматирования таблицы...")
    
    # Получаем отсортированные данные
    products = test_data_transformation()
    api = MayakAPI()
    sorted_products = api.sort_products_by_sales(products, reverse=True)
    
    # Форматируем таблицу
    table = api.format_products_table(sorted_products)
    
    if "ТОВАРЫ ПО ПРОДАЖАМ" in table and "ID товара" in table:
        print("✅ Форматирование таблицы работает")
        print("\nПример таблицы:")
        print(table)
        return True
    else:
        print("❌ Форматирование таблицы не работает")
        return False


def test_integration_with_parser():
    """Тест интеграции с основным парсером"""
    print("\n🧪 Тест интеграции с WBParser...")
    
    # Создаем парсер без cookies (для демо)
    parser = WBParser()
    
    # Тестируем метод отображения
    products = test_data_transformation()
    api = MayakAPI()
    sorted_products = api.sort_products_by_sales(products, reverse=True)
    
    # Создаем парсер с API для тестирования метода
    parser_with_api = WBParser()
    parser_with_api.mayak_api = api
    
    display_result = parser_with_api.display_products_by_sales(sorted_products, limit=3)
    
    if "ТОВАРЫ ПО ПРОДАЖАМ" in display_result:
        print("✅ Интеграция с WBParser работает")
        print("Пример вывода с ограничением в 3 товара:")
        print(display_result)
        return True
    else:
        print("❌ Интеграция с WBParser не работает")
        return False


def demo_real_data_structure():
    """Демонстрация работы с реальной структурой данных"""
    print("\n🎯 ДЕМО: Структура данных Mayak API")
    print("=" * 50)
    
    # Пример реального ответа
    real_response = {
        "64775386": {
            "sales": 7193,
            "revenue": 19747579,
            "lost_revenue": 11161879,
            "avg_price": 2689
        },
        "306897066": {
            "sales": 12450,
            "revenue": 35678901,
            "lost_revenue": 8765432,
            "avg_price": 2867
        },
        "164105063": {
            "sales": 3456,
            "revenue": 9876543,
            "lost_revenue": 2345678,
            "avg_price": 2856
        }
    }
    
    print("📥 Исходный формат данных от Mayak API:")
    print(json.dumps(real_response, indent=2, ensure_ascii=False))
    
    print("\n🔄 После преобразования и сортировки:")
    products_list = []
    for product_id, product_data in real_response.items():
        product_info = product_data.copy()
        product_info['id'] = product_id
        products_list.append(product_info)
    
    api = MayakAPI()
    sorted_products = api.sort_products_by_sales(products_list, reverse=True)
    
    print(api.format_products_table(sorted_products))


def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование сортировки по продажам")
    print("=" * 60)
    
    tests = [
        test_sales_sorting,
        test_table_formatting,
        test_integration_with_parser
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Результат тестирования: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты прошли успешно!")
    else:
        print("⚠️  Некоторые тесты не прошли")
    
    # Показываем демо независимо от результатов тестов
    demo_real_data_structure()
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
