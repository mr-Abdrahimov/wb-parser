#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест генерации ссылок на изображения WildBerries
"""

from wb_parser import WBParser


def test_image_url_generation():
    """Тест генерации ссылок на изображения"""
    print("🧪 Тест генерации ссылок на изображения...")
    
    parser = WBParser()
    
    # Тестовые случаи на основе реальных ID
    test_cases = [
        {
            'product_id': 164105063,
            'pics': 8,
            'expected_vol': 1641,
            'expected_part': 164105,
            'expected_host': '11'  # vol 1641 попадает в диапазон 1602-1655 = host 11
        },
        {
            'product_id': 306897066,
            'pics': 13,
            'expected_vol': 3068,
            'expected_part': 306897,
            'expected_host': '19'  # vol 3068 > 2447 = host 19
        },
        {
            'product_id': 64775386,
            'pics': 5,
            'expected_vol': 647,
            'expected_part': 64775,
            'expected_host': '04'  # vol 647 попадает в диапазон 432-719 = host 04
        }
    ]
    
    all_passed = True
    
    for i, case in enumerate(test_cases, 1):
        product_id = case['product_id']
        pics = case['pics']
        expected_vol = case['expected_vol']
        expected_part = case['expected_part']
        expected_host = case['expected_host']
        
        print(f"\n  Тест {i}: ID {product_id}, {pics} изображений")
        
        # Генерируем ссылки
        image_urls = parser.generate_image_urls(product_id, pics)
        
        # Проверяем количество ссылок
        if len(image_urls) != pics:
            print(f"    ❌ Неверное количество ссылок: {len(image_urls)} вместо {pics}")
            all_passed = False
            continue
        
        # Проверяем первую ссылку
        first_url = image_urls[0]
        expected_first_url = f"https://basket-{expected_host}.wbbasket.ru/vol{expected_vol}/part{expected_part}/{product_id}/images/big/1.webp"
        
        if first_url == expected_first_url:
            print(f"    ✅ Первая ссылка корректна: {first_url}")
        else:
            print(f"    ❌ Первая ссылка неверна:")
            print(f"       Получено: {first_url}")
            print(f"       Ожидалось: {expected_first_url}")
            all_passed = False
            continue
        
        # Проверяем последнюю ссылку
        if pics > 1:
            last_url = image_urls[-1]
            expected_last_url = f"https://basket-{expected_host}.wbbasket.ru/vol{expected_vol}/part{expected_part}/{product_id}/images/big/{pics}.webp"
            
            if last_url == expected_last_url:
                print(f"    ✅ Последняя ссылка корректна: {last_url}")
            else:
                print(f"    ❌ Последняя ссылка неверна:")
                print(f"       Получено: {last_url}")
                print(f"       Ожидалось: {expected_last_url}")
                all_passed = False
        
        print(f"    📊 Всего ссылок: {len(image_urls)}")
    
    return all_passed


def test_edge_cases():
    """Тест граничных случаев"""
    print("\n🧪 Тест граничных случаев...")
    
    parser = WBParser()
    
    # Случай с 0 изображений
    urls_zero = parser.generate_image_urls(123456789, 0)
    if len(urls_zero) == 0:
        print("  ✅ Корректная обработка 0 изображений")
    else:
        print(f"  ❌ Неверная обработка 0 изображений: получено {len(urls_zero)} ссылок")
        return False
    
    # Случай с большим количеством изображений
    urls_many = parser.generate_image_urls(123456789, 25)
    if len(urls_many) == 25:
        print("  ✅ Корректная обработка большого количества изображений")
    else:
        print(f"  ❌ Неверная обработка большого количества: получено {len(urls_many)} вместо 25")
        return False
    
    return True


def demo_real_urls():
    """Демонстрация реальных ссылок"""
    print("\n🎯 ДЕМО: Реальные ссылки на изображения")
    print("=" * 60)
    
    parser = WBParser()
    
    # Используем реальный ID из примера пользователя
    real_id = 164105063
    pics_count = 8
    
    print(f"Товар ID: {real_id}")
    print(f"Количество изображений: {pics_count}")
    print()
    
    # Показываем расчеты
    vol = real_id // 100000
    part = real_id // 1000
    print(f"vol = {real_id} // 100000 = {vol}")
    print(f"part = {real_id} // 1000 = {part}")
    print(f"Сервер для vol {vol}: basket-11 (диапазон 1602-1655)")
    print()
    
    # Генерируем ссылки
    image_urls = parser.generate_image_urls(real_id, pics_count)
    
    print("🖼️ Сгенерированные ссылки:")
    for i, url in enumerate(image_urls, 1):
        print(f"  {i}. {url}")
    
    print(f"\n📊 Всего сгенерировано: {len(image_urls)} ссылок")
    
    # Проверим, что первая ссылка соответствует примеру пользователя
    expected_url = "https://basket-11.wbbasket.ru/vol1641/part164105/164105063/images/big/1.webp"
    if image_urls[0] == expected_url:
        print("✅ Первая ссылка соответствует примеру пользователя!")
    else:
        print("❌ Первая ссылка не соответствует примеру")
        print(f"Ожидалось: {expected_url}")
        print(f"Получено:  {image_urls[0]}")


def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование генерации ссылок на изображения WB")
    print("=" * 70)
    
    tests = [
        test_image_url_generation,
        test_edge_cases
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 70)
    print(f"📊 Результат тестирования: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты прошли успешно!")
    else:
        print("⚠️  Некоторые тесты не прошли")
    
    # Показываем демо
    demo_real_urls()
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
