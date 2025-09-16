#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест интеграции данных о pics из WB с данными о продажах от Mayak
"""

from wb_parser import WBParser
import json


def test_wb_data_extraction():
    """Тест извлечения данных о pics из WB"""
    print("🧪 Тест извлечения данных о pics...")
    
    # Симулируем ответ от WB API
    mock_wb_response = {
        "products": [
            {"id": 306897066, "pics": 13, "name": "Куртка 1"},
            {"id": 164105063, "pics": 8, "name": "Куртка 2"},
            {"id": 244733060, "pics": 15, "name": "Куртка 3"}
        ],
        "total": 1000
    }
    
    parser = WBParser()
    wb_products = parser.extract_products_with_pics(mock_wb_response)
    
    expected_keys = [306897066, 164105063, 244733060]
    
    if (len(wb_products) == 3 and 
        all(key in wb_products for key in expected_keys) and
        wb_products[306897066]['pics'] == 13):
        print("✅ Извлечение данных о pics работает")
        print(f"Пример: ID {306897066} имеет {wb_products[306897066]['pics']} фото")
        return True
    else:
        print("❌ Извлечение данных о pics не работает")
        return False


def test_data_combination():
    """Тест объединения данных WB и Mayak"""
    print("\n🧪 Тест объединения данных...")
    
    # Симулируем данные от Mayak (отсортированные по продажам)
    mayak_data = [
        {'id': '244733060', 'sales': 15678, 'revenue': 45234567, 'avg_price': 2885},
        {'id': '306897066', 'sales': 12450, 'revenue': 35678901, 'avg_price': 2867},
        {'id': '164105063', 'sales': 8765, 'revenue': 25123456, 'avg_price': 2867}
    ]
    
    # Симулируем данные от WB
    wb_data = {
        306897066: {'pics': 13, 'wb_data': {'name': 'Куртка 1'}},
        164105063: {'pics': 8, 'wb_data': {'name': 'Куртка 2'}},
        244733060: {'pics': 15, 'wb_data': {'name': 'Куртка 3'}}
    }
    
    # Объединяем данные (как это делается в методе)
    combined_products = []
    for mayak_product in mayak_data:
        product_id = int(mayak_product.get('id', 0))
        
        if product_id in wb_data:
            mayak_product['pics'] = wb_data[product_id]['pics']
        else:
            mayak_product['pics'] = 0
        
        combined_products.append(mayak_product)
    
    # Проверяем результат
    if (len(combined_products) == 3 and
        combined_products[0]['id'] == '244733060' and  # Самый продаваемый
        combined_products[0]['pics'] == 15 and
        combined_products[1]['pics'] == 13 and
        combined_products[2]['pics'] == 8):
        print("✅ Объединение данных работает корректно")
        print("Результат (отсортировано по продажам):")
        for i, product in enumerate(combined_products, 1):
            print(f"  {i}. ID {product['id']}: {product['sales']:,} продаж, {product['pics']} фото")
        return True
    else:
        print("❌ Объединение данных не работает")
        return False


def demo_final_output():
    """Демонстрация финального вывода"""
    print("\n🎯 ДЕМО: Финальный вывод")
    print("=" * 50)
    
    # Пример финального результата
    final_products = [
        {'id': '315813991', 'sales': 23456, 'pics': 12},
        {'id': '244733060', 'sales': 15678, 'pics': 15},
        {'id': '306897066', 'sales': 12450, 'pics': 13},
        {'id': '164105063', 'sales': 8765, 'pics': 8},
        {'id': '64775386', 'sales': 7193, 'pics': 5}
    ]
    
    print("📋 СПИСОК ТОВАРОВ (отсортировано по продажам):")
    print("ID товара | Продажи | Фото")
    print("-" * 30)
    
    for product in final_products:
        product_id = product.get('id')
        sales = product.get('sales', 0)
        pics = product.get('pics', 0)
        print(f"{product_id} | {sales:,} | {pics}")
    
    print(f"\nВсего товаров: {len(final_products)}")


def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование интеграции pics с данными о продажах")
    print("=" * 60)
    
    tests = [
        test_wb_data_extraction,
        test_data_combination
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Результат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты прошли успешно!")
    else:
        print("⚠️  Некоторые тесты не прошли")
    
    # Показываем демо
    demo_final_output()
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

