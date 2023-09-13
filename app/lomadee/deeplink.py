from urllib.parse import quote
import aiohttp
from app.settings import LOMADEE_APP_TOKEN, LOMADEE_SOURCE_ID


async def get_afiliate_url(url: str) -> str:
  encoded_url = quote(url)
  lomadee_deep_link_url = f"https://api.lomadee.com/v2/1692298135285757b7f2b/deeplink/_create?app-token={LOMADEE_APP_TOKEN}&sourceId={LOMADEE_SOURCE_ID}&url={encoded_url}&domain=oferta.vc"
  async with aiohttp.ClientSession() as session:
    async with session.get(lomadee_deep_link_url) as res:
      if res.status != 200: raise Exception("Failed to generate afiliate link")
      data = await res.json()
      afiliate_url = data['deeplinks'][0]['deeplink']
      return afiliate_url

