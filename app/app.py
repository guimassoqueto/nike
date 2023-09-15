from asyncio import Semaphore
from app.handlers.parser import NikeParser
from app.infra.psycopg.postgres import insert_products
from app.settings import NIKE_OFFERS_API
from app.logging.logger import getLogger
from app.infra.aiohttp.aiohttp import AioHttpRetry
import math


logger = getLogger("app.py")


async def get_urls() -> list:
  data = await AioHttpRetry.get_json(NIKE_OFFERS_API)
  products_per_pages = data['pageProps']['dehydratedState']['queries'][0]['state']['data']['pages'][0]['productsPerPage']
  total_products = data['pageProps']['dehydratedState']['queries'][0]['state']['data']['pages'][0]['quantity']
  total_pages = math.ceil(total_products / products_per_pages) + 1
  urls = [ NIKE_OFFERS_API.replace("&page=1", f"&page={i}") for i in range(1, total_pages) ]
  return urls



async def application(url: str, concurrency_limit: Semaphore) -> None:
  async with concurrency_limit:
    data = await AioHttpRetry.get_json(url)
    products = await NikeParser.get_products(data)
    await insert_products(products)
