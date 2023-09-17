from dotenv import load_dotenv
from os import getenv
load_dotenv()

# Postgres connection
POSTGRES_DB = getenv("POSTGRES_DB", "postgres")
POSTGRES_HOST = getenv("POSTGRES_HOST", "localhost")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "password")
POSTGRES_PORT = getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = getenv("POSTGRES_USER", "postgres")
TABLE_NAME = getenv("TABLE_NAME", "sports")

# max requests concurrency
MAX_CONCURRENCY = int(getenv("MAX_CONCURRENCY", 8))

# nike products api to get the json
NIKE_OFFERS_API = getenv("NIKE_OFFERS_API", "")

# Lomadde
LOMADEE_APP_TOKEN = getenv("LOMADEE_APP_TOKEN", "")
LOMADEE_SOURCE_ID = getenv("LOMADEE_SOURCE_ID", "")

# Scrapeops rotating proxy: https://scrapeops.io/app/proxy
SCRAPEOPS_APY_KEY=getenv("SCRAPEOPS_APY_KEY", "")