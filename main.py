from asyncio import Semaphore, run, create_task, gather
from app.errors.unexpected_status_error import UnexpectedStatusError
from app.settings import MAX_CONCURRENCY
from app.app import application, get_urls


concurrency_limit = Semaphore(MAX_CONCURRENCY)


async def main(concurrency_limit: Semaphore):
  urls = await get_urls()
  tasks = []
  for url in urls:
      task = create_task(application(url, concurrency_limit))
      tasks.append(task)
  result = await gather(*tasks)
  return result


if __name__ == "__main__":
    try:
      run(main(concurrency_limit=concurrency_limit))
    
    except UnexpectedStatusError as e:
      print(e)

    except Exception as e:
      print("error", e)
