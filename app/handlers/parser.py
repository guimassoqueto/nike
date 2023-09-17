from urllib.parse import urljoin
from app.domain.model import Item
from app.handlers.helpers import get_afiliate_url
from app.logging.logger import getLogger
import re


logger = getLogger("parser.py")


class NikeParser:
  @staticmethod
  async def get_products(data: dict) -> list[dict]:
    raw_products = data['pageProps']['dehydratedState']['queries'][0]['state']['data']['pages'][0]['products']
    products = []
    for product in raw_products:
      
      try:
        details = product["details"]

        is_available = product["details"]["hasStock"]
        if not is_available: continue

        title = str(product['name']).replace("'", "''").strip()
        if not re.search('tênis', title, re.IGNORECASE): continue
        if re.search('infantil', title, re.IGNORECASE): continue

        category = f"{details['modality']} {' '.join(details['categories'])} {' '.join(details['genders'])}"
        if re.search('infantil', category, re.IGNORECASE): continue

        price = product['price']
        previous_price = product['oldPrice']
        discount = round((1 - (price / previous_price)) * 100)
        if discount < 40: continue

        url = urljoin('https://www.nike.com.br/', product['url']).replace("'", "''")
        afiliate_url = await get_afiliate_url(url)
        image_url = f"https://imgnike-a.akamaihd.net/1080x1080/{product['id']}.jpg"

        item = Item(
          url=url,
          afiliate_url=afiliate_url,
          title=title,
          category=category,
          image_url=image_url,
          price=price,
          free_shipping=False,
          reviews=0,
          previous_price=previous_price,
          discount=discount
        )

        products.append(item.model_dump())
      except Exception as e:
        logger.warning(e)
        continue
    return products
