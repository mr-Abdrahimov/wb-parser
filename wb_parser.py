#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WildBerries Parser
Программа для парсинга товаров с WildBerries через их API
"""

import requests
import json
import urllib.parse
from typing import List, Optional, Dict, Any
import logging
from mayak_api import MayakAPI

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WBParser:
    """Класс для парсинга данных с WildBerries"""

    BASE_URL = "https://search.wb.ru/exactmatch/ru/common/v18/search"

    DEFAULT_PARAMS = {
        "ab_testing": "false",
        "appType": "64",
        "curr": "rub",
        "dest": "12358327",
        "hide_dflags": "131072",
        "inheritFilters": "false",
        "lang": "ru",
        "page": "1",
        "resultset": "catalog",
        "sort": "popular",
        "spp": "30",
        "suppressSpellcheck": "false"
    }

    def __init__(self, mayak_cookies: Optional[str] = None):
        self.session = requests.Session()
        # Добавляем заголовки для имитации браузера
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })

        # Инициализируем Mayak API клиент если переданы cookies
        self.mayak_api = None
        if mayak_cookies:
            self.mayak_api = MayakAPI(mayak_cookies)

    def build_url(self, query: str, page: int = 1) -> str:
        """
        Формирует URL для запроса к API WildBerries

        Args:
            query: Поисковый запрос
            page: Номер страницы (по умолчанию 1)

        Returns:
            Сформированный URL
        """
        params = self.DEFAULT_PARAMS.copy()
        params["query"] = query
        params["page"] = str(page)

        # Кодируем параметры для URL
        encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        url = f"{self.BASE_URL}?{encoded_params}"

        logger.info(f"Сформирован URL: {url}")
        return url

    def fetch_data(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Выполняет HTTP запрос и возвращает JSON данные

        Args:
            url: URL для запроса

        Returns:
            Словарь с данными или None в случае ошибки
        """
        try:
            logger.info(f"Выполняется запрос к: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()
            logger.info(f"Получен ответ, размер: {len(response.text)} символов")
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при выполнении запроса: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка при парсинге JSON: {e}")
            return None

    def extract_product_ids(self, data: Dict[str, Any]) -> List[int]:
        """
        Извлекает ID продуктов из JSON ответа

        Args:
            data: Словарь с данными от API

        Returns:
            Список ID продуктов
        """
        product_ids = []

        try:
            products = data.get("products", [])
            if not products:
                logger.warning("В ответе не найден массив products или он пустой")
                return product_ids

            for product in products:
                if isinstance(product, dict) and "id" in product:
                    product_ids.append(product["id"])

            logger.info(f"Извлечено {len(product_ids)} ID продуктов")
            return product_ids

        except Exception as e:
            logger.error(f"Ошибка при извлечении ID продуктов: {e}")
            return product_ids

    def extract_products_with_pics(self, data: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
        """
        Извлекает продукты с информацией о количестве изображений

        Args:
            data: Словарь с данными от WB API

        Returns:
            Словарь {id: {pics: количество, ...другие данные}}
        """
        products_info = {}

        try:
            products = data.get("products", [])
            if not products:
                logger.warning("В ответе не найден массив products или он пустой")
                return products_info

            for product in products:
                if isinstance(product, dict) and "id" in product:
                    product_id = product["id"]
                    pics_count = product.get("pics", 0)

                    products_info[product_id] = {
                        "pics": pics_count,
                        "wb_data": product  # Сохраняем полные данные от WB
                    }

            logger.info(f"Извлечено {len(products_info)} продуктов с информацией об изображениях")
            return products_info

        except Exception as e:
            logger.error(f"Ошибка при извлечении информации о продуктах: {e}")
            return products_info

    def search_products(self, query: str, page: int = 1) -> List[int]:
        """
        Основная функция для поиска продуктов и получения их ID

        Args:
            query: Поисковый запрос
            page: Номер страницы

        Returns:
            Список ID продуктов
        """
        logger.info(f"Начинаем поиск по запросу: '{query}', страница: {page}")

        url = self.build_url(query, page)
        data = self.fetch_data(url)

        if data is None:
            logger.error("Не удалось получить данные")
            return []

        product_ids = self.extract_product_ids(data)
        return product_ids

    def get_total_products(self, query: str) -> int:
        """
        Получает общее количество найденных продуктов

        Args:
            query: Поисковый запрос

        Returns:
            Общее количество продуктов
        """
        url = self.build_url(query, 1)
        data = self.fetch_data(url)

        if data is None:
            return 0

        return data.get("total", 0)

    def get_products_detailed_info(self, product_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Получает подробную информацию о товарах через Mayak API

        Args:
            product_ids: Список ID товаров

        Returns:
            Список с подробной информацией о товарах
        """
        if not self.mayak_api:
            logger.error("Mayak API не инициализирован. Передайте cookies в конструктор.")
            return []

        products = self.mayak_api.get_all_products_info(product_ids)

        # Сортируем по продажам (от большего к меньшему)
        if products:
            products = self.mayak_api.sort_products_by_sales(products, reverse=True)

        return products

    def get_products_detailed_info_with_pics(self, query: str, page: int = 1, max_products: int = None) -> List[
        Dict[str, Any]]:
        """
        Получает подробную информацию о товарах с добавлением данных об изображениях из WB

        Args:
            query: Поисковый запрос
            page: Номер страницы
            max_products: Максимальное количество товаров

        Returns:
            Список товаров с объединенными данными от WB и Mayak
        """
        if not self.mayak_api:
            logger.error("Mayak API не инициализирован. Передайте cookies в конструктор.")
            return []

        # Получаем данные от WB
        url = self.build_url(query, page)
        wb_data = self.fetch_data(url)

        if not wb_data:
            return []

        # Извлекаем продукты с информацией об изображениях
        wb_products = self.extract_products_with_pics(wb_data)
        product_ids = list(wb_products.keys())

        # Ограничиваем количество если указано
        if max_products and len(product_ids) > max_products:
            product_ids = product_ids[:max_products]
            logger.info(f"Ограничено до {max_products} товаров")

        # Получаем подробную информацию от Mayak
        mayak_products = self.mayak_api.get_all_products_info(product_ids)

        # Сортируем по продажам
        if mayak_products:
            mayak_products = self.mayak_api.sort_products_by_sales(mayak_products, reverse=True)

        # Объединяем данные
        combined_products = []
        for mayak_product in mayak_products:
            product_id = int(mayak_product.get('id', 0))

            # Добавляем данные из WB
            if product_id in wb_products:
                pics_count = wb_products[product_id]['pics']
                mayak_product['pics'] = pics_count

                # Генерируем ссылки на изображения
                image_urls = self.generate_image_urls(product_id, pics_count)
                mayak_product['image_urls'] = image_urls

                # Добавляем название из WB (если есть)
                wb_full = wb_products[product_id].get('wb_data', {})
                if isinstance(wb_full, dict):
                    mayak_product['name'] = wb_full.get('name', '')
                else:
                    mayak_product['name'] = ''

                # Можно добавить и другие данные из WB если нужно
                # mayak_product['wb_brand'] = wb_full.get('brand', '')
            else:
                mayak_product['pics'] = 0  # Если данных нет, ставим 0
                mayak_product['image_urls'] = []
                mayak_product['name'] = ''

            combined_products.append(mayak_product)

        logger.info(f"Объединено {len(combined_products)} товаров с данными WB и Mayak")
        return combined_products

    def generate_image_urls(self, product_id: int, pics_count: int) -> List[str]:
        """
        Генерирует ссылки на изображения товара WildBerries

        Args:
            product_id: ID товара
            pics_count: Количество изображений

        Returns:
            Список ссылок на изображения
        """
        if pics_count <= 0:
            return []

        # Определяем vol (обрезаем последние 5 цифр)
        vol = product_id // 100000

        # Определяем номер сервера по vol (новые диапазоны)
        def get_basket_host(vol):
            if 0 <= vol <= 143:
                return "01"
            elif vol <= 287:
                return "02"
            elif vol <= 431:
                return "03"
            elif vol <= 719:
                return "04"
            elif vol <= 1007:
                return "05"
            elif vol <= 1061:
                return "06"
            elif vol <= 1115:
                return "07"
            elif vol <= 1169:
                return "08"
            elif vol <= 1313:
                return "09"
            elif vol <= 1601:
                return "10"
            elif vol <= 1655:
                return "11"
            elif vol <= 1919:
                return "12"
            elif vol <= 2045:
                return "13"
            elif vol <= 2189:
                return "14"
            elif vol <= 2405:
                return "15"
            elif vol <= 2621:
                return "16"
            elif vol <= 2837:
                return "17"
            elif vol <= 3053:
                return "18"
            elif vol <= 3269:
                return "19"
            elif vol <= 3485:
                return "20"
            elif vol <= 3701:
                return "21"
            elif vol <= 3917:
                return "22"
            elif vol <= 4133:
                return "23"
            elif vol <= 4349:
                return "24"
            elif vol <= 4565:
                return "25"
            elif vol <= 4877:
                return "26"
            elif vol <= 5189:
                return "27"
            elif vol <= 5501:
                return "28"
            elif vol <= 5813:
                return "29"
            elif vol <= 6125:
                return "30"
            elif vol <= 6437:
                return "31"
            else:
                return "32"

        basket_host = get_basket_host(vol)
        part = product_id // 1000  # part это ID без последних 3 цифр

        # Генерируем ссылки на все изображения
        image_urls = []
        for i in range(1, pics_count + 1):
            url = f"https://basket-{basket_host}.wbbasket.ru/vol{vol}/part{part}/{product_id}/images/big/{i}.webp"
            image_urls.append(url)

        logger.info(f"Сгенерировано {len(image_urls)} ссылок на изображения для товара {product_id}")
        return image_urls

    def search_and_get_detailed_info(self, query: str, page: int = 1, max_products: int = None) -> Dict[str, Any]:
        """
        Выполняет поиск и получает подробную информацию о найденных товарах

        Args:
            query: Поисковый запрос
            page: Номер страницы
            max_products: Максимальное количество товаров для получения подробной информации

        Returns:
            Словарь с результатами поиска и подробной информацией
        """
        # Получаем ID товаров
        product_ids = self.search_products(query, page)

        if not product_ids:
            return {
                'query': query,
                'page': page,
                'found_ids': [],
                'detailed_info': []
            }

        # Ограничиваем количество если указано
        if max_products and len(product_ids) > max_products:
            product_ids = product_ids[:max_products]
            logger.info(f"Ограничено до {max_products} товаров")

        # Получаем подробную информацию
        detailed_info = self.get_products_detailed_info(product_ids)

        return {
            'query': query,
            'page': page,
            'found_ids': product_ids,
            'detailed_info': detailed_info,
            'total_found': len(product_ids),
            'total_detailed': len(detailed_info)
        }

    def display_products_by_sales(self, products: List[Dict[str, Any]], limit: int = None) -> str:
        """
        Отображает товары в виде таблицы, отсортированной по продажам

        Args:
            products: Список товаров с данными о продажах
            limit: Ограничение количества товаров для отображения

        Returns:
            Форматированная таблица
        """
        if not self.mayak_api:
            return "❌ Mayak API не инициализирован"

        return self.mayak_api.format_products_table(products, limit)


def main():
    """Основная функция программы"""
    parser = WBParser()

    # Пример использования
    query = "куртка женская черная"

    print(f"Поиск продуктов по запросу: '{query}'")
    print("-" * 50)

    # Получаем общее количество продуктов
    total = parser.get_total_products(query)
    print(f"Всего найдено продуктов: {total}")

    # Получаем ID продуктов с первой страницы
    product_ids = parser.search_products(query, page=1)

    if product_ids:
        print(f"\nНайдено {len(product_ids)} ID продуктов на первой странице:")
        for i, product_id in enumerate(product_ids, 1):
            print(f"{i}. {product_id}")
    else:
        print("Продукты не найдены")


if __name__ == "__main__":
    main()
