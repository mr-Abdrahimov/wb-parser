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
    
    def __init__(self):
        self.session = requests.Session()
        # Добавляем заголовки для имитации браузера
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
    
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
