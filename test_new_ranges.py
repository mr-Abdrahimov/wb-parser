#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест новых диапазонов серверов WildBerries
"""

from wb_parser import WBParser


def test_server_ranges():
    """Тест всех диапазонов серверов"""
    print("🧪 Тест новых диапазонов серверов WB...")
    
    parser = WBParser()
    
    # Тестовые случаи для разных диапазонов
    test_ranges = [
        # Граничные значения для каждого сервера
        (0, "01"),      # 0 <= vol <= 143
        (143, "01"),
        (144, "02"),    # vol <= 287
        (287, "02"),
        (288, "03"),    # vol <= 431
        (431, "03"),
        (432, "04"),    # vol <= 719
        (719, "04"),
        (720, "05"),    # vol <= 1007
        (1007, "05"),
        (1008, "06"),   # vol <= 1061
        (1061, "06"),
        (1062, "07"),   # vol <= 1115
        (1115, "07"),
        (1116, "08"),   # vol <= 1169
        (1169, "08"),
        (1170, "09"),   # vol <= 1313
        (1313, "09"),
        (1314, "10"),   # vol <= 1601
        (1601, "10"),
        (1602, "11"),   # vol <= 1655
        (1655, "11"),
        (1656, "12"),   # vol <= 1919
        (1919, "12"),
        (1920, "13"),   # vol <= 2045
        (2045, "13"),
        (2046, "14"),   # vol <= 2189
        (2189, "14"),
        (2190, "15"),   # vol <= 2405
        (2405, "15"),
        (2406, "16"),   # vol <= 2621
        (2621, "16"),
        (2622, "17"),   # vol <= 2837
        (2837, "17"),
        (2838, "18"),   # vol <= 3053
        (3053, "18"),
        (3054, "19"),   # vol <= 3269
        (3269, "19"),
        (3270, "20"),   # vol <= 3485
        (3485, "20"),
        (3486, "21"),   # vol <= 3701
        (3701, "21"),
        (3702, "22"),   # vol <= 3917
        (3917, "22"),
        (3918, "23"),   # vol <= 4133
        (4133, "23"),
        (4134, "24"),   # vol <= 4349
        (4349, "24"),
        (4350, "25"),   # vol <= 4565
        (4565, "25"),
        (4566, "26"),   # vol <= 4877
        (4877, "26"),
        (4878, "27"),   # vol <= 5189
        (5189, "27"),
        (5190, "28"),   # vol <= 5501
        (5501, "28"),
        (5502, "29"),   # vol <= 5813
        (5813, "29"),
        (5814, "30"),   # vol <= 6125
        (6125, "30"),
        (6126, "31"),   # vol <= 6437
        (6437, "31"),
        (6438, "32"),   # default
        (10000, "32"),  # большое значение
    ]
    
    all_passed = True
    failed_cases = []
    
    for vol, expected_host in test_ranges:
        # Создаем тестовый product_id
        product_id = vol * 100000 + 12345  # добавляем 5 цифр
        
        # Генерируем одну ссылку
        image_urls = parser.generate_image_urls(product_id, 1)
        
        if not image_urls:
            failed_cases.append(f"vol {vol}: не сгенерированы ссылки")
            all_passed = False
            continue
        
        # Проверяем хост в ссылке
        url = image_urls[0]
        expected_part = f"basket-{expected_host}.wbbasket.ru"
        
        if expected_part in url:
            print(f"  ✅ vol {vol:>4} → basket-{expected_host}")
        else:
            print(f"  ❌ vol {vol:>4} → ожидался basket-{expected_host}, получен: {url}")
            failed_cases.append(f"vol {vol}: ожидался {expected_host}")
            all_passed = False
    
    print(f"\n📊 Результат: {len(test_ranges) - len(failed_cases)}/{len(test_ranges)} тестов прошли")
    
    if failed_cases:
        print("\n❌ Неудачные тесты:")
        for case in failed_cases:
            print(f"  - {case}")
    else:
        print("🎉 Все диапазоны работают корректно!")
    
    return all_passed


def demo_new_servers():
    """Демонстрация новых серверов"""
    print("\n🎯 ДЕМО: Новые серверы WildBerries")
    print("=" * 50)
    
    parser = WBParser()
    
    demo_cases = [
        (500012345, "Сервер 27 (vol 5000)"),
        (320012345, "Сервер 19 (vol 3200)"),  
        (450012345, "Сервер 24 (vol 4500)"),
        (600012345, "Сервер 29 (vol 6000)"),
        (700012345, "Сервер 32 (vol 7000, default)"),
    ]
    
    for product_id, description in demo_cases:
        vol = product_id // 100000
        image_urls = parser.generate_image_urls(product_id, 2)
        
        if image_urls:
            print(f"\n{description}:")
            print(f"  ID: {product_id}")
            print(f"  vol: {vol}")
            print(f"  Ссылки:")
            for i, url in enumerate(image_urls, 1):
                print(f"    {i}. {url}")


def main():
    """Основная функция"""
    print("🚀 Тестирование новых диапазонов серверов WB")
    print("=" * 60)
    
    success = test_server_ranges()
    demo_new_servers()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Все новые диапазоны работают корректно!")
    else:
        print("⚠️  Обнаружены проблемы с некоторыми диапазонами")
    
    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
