from app.errors.unexpected_status_error import UnexpectedStatusError
from app.infra.aiohttp.helpers import header
from aiohttp_retry import RetryClient, RequestParams

class AioHttpRetry:
  @staticmethod
  async def get_json(url: str) -> dict:
    async with RetryClient() as client:
        async with client.requests(params_list=[RequestParams(method="GET", url=url, headers=header())]        ) as response:
          if response.status > 400 and response.status < 500: raise UnexpectedStatusError(response.status)
          return await response.json()
