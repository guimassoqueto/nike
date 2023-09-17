from fake_useragent import UserAgent
from urllib.parse import quote


def header() -> dict:
  return {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection':	'keep-alive',
    'Host':	'www.nike.com.br',
    'If-None-Match': "2473a-/sPrqiNGsqYIZeDxEz+87lTUt3M",
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'TE':	'trailers',
    'Upgrade-Insecure-Requests':	'1',
    'User-Agent': UserAgent().random
  }


def encode_url(url: str) -> str:
  return quote(url)