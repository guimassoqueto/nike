from asyncio import Semaphore
from urllib.parse import urljoin
from app.psycopg.postgres import insert_products
from app.model.item import Item
from app.settings import NIKE_OFFERS_API
from app.lomadee.deeplink import get_afiliate_url
from app.logging.logger import getLogger
from app.infra.aiohttp.aiohttp import AioHttpRetry
import math
import re


logger = getLogger("app.py")


def get_nike_api_url(page_number: int):
    url = NIKE_OFFERS_API.replace("&page=", f"&page={page_number}")
    return url


async def get_urls() -> list:
    url = get_nike_api_url(0)
    try:
        data = await AioHttpRetry.get_json(url)
        products_per_pages = data['pageProps']['dehydratedState']['queries'][0]['state']['data']['pages'][0]['productsPerPage']
        total_products = data['pageProps']['dehydratedState']['queries'][0]['state']['data']['pages'][0]['quantity']
        total_pages = math.ceil(total_products / products_per_pages) + 1
        return [ get_nike_api_url(i) for i in range(0, total_pages) ]
    except Exception as e:
        logger.error(e)
        return [ url ]


class ScraperNike:
    async def scrap(self, url: str, concurrency_limit: Semaphore) -> None:
        async with concurrency_limit:
            try:
                data = await AioHttpRetry.get_json(url)
                products = await self.parse_data(data)
                await insert_products(products)
            except Exception as e:
                logger.error(e)


    async def parse_data(self, data) -> list:
        products_raw = data['pageProps']['dehydratedState']['queries'][0]['state']['data']['pages'][0]['products']
        products = []
        for product in products_raw:
            try:
                has_stock = product["details"]["hasStock"]
                if has_stock:
                  item = await self.format_item(product)
                  if item: products.append(item)
            except Exception as e:
                logger.error(e)
                continue
        return products
    

    async def format_item(self, product: dict) -> dict | None:
        details = product["details"]
        title = str(product['name']).replace("'", "''").strip()
        url = urljoin('https://www.nike.com.br/', product['url']).replace("'", "''")
        image_url = f"https://imgnike-a.akamaihd.net/1080x1080/{product['id']}.jpg"
        category = f"{details['modality']} {' '.join(details['categories'])} {' '.join(details['genders'])}"
        price = product['price']
        previous_price = product['oldPrice']
        discount = round((1 - (price / previous_price)) * 100)

        if not re.search('tênis', title, re.IGNORECASE): return None
        if re.search('infantil', title, re.IGNORECASE): return None
        if re.search('infantil', category, re.IGNORECASE): return None
        if discount < 40: return None

        afiliate_url = await get_afiliate_url(url)
        
        item = Item(
            url=url,
            afiliate_url=afiliate_url,
            title=title,
            category=category,
            image_url=image_url,
            price=price,
            previous_price=previous_price,
            discount=discount
        )
        return item.model_dump()
