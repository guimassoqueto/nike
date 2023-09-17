from app.errors.unexpected_status_error import UnexpectedStatusError
from app.infra.aiohttp.helpers import encode_url, header
from app.settings import SCRAPEOPS_APY_KEY
from aiohttp_retry import RetryClient, RequestParams
from aiohttp import ClientSession


class AioHttpRetry:
  @staticmethod
  async def get_json(url: str) -> dict:
    async with RetryClient() as client:
        async with client.requests(params_list=[RequestParams(method="GET", url=url, headers=header())]) as response:
          if response.status > 400 and response.status < 500: raise UnexpectedStatusError(response.status)
          return await response.json()


## TODO: Serviço de requisição com rotação de ip
class AioHttpProxy:
  @staticmethod
  async def get_json(url: str) -> dict:
    encoded_url = encode_url(url)
    async with ClientSession() as session:
      async with session.get(f'https://proxy.scrapeops.io/v1?api_key={SCRAPEOPS_APY_KEY}&url={encoded_url}') as response:
        if response.status > 400 and response.status < 500: raise UnexpectedStatusError(response.status)
        return await response.json()
      
