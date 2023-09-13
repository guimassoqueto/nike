from asyncio import Semaphore, run
from app.errors.errors import APIHasChangedError
from app.settings import MAX_CONCURRENCY
from app.client_code.parser import Nike


concurrency_limit = Semaphore(MAX_CONCURRENCY)


def write_error(message: str):
    with open("error.txt", "+a", encoding="utf-8") as f:
        f.write(f"ERROR: {message}\n")


if __name__ == "__main__":
    try:
      run(Nike.exec(concurrency_limit=concurrency_limit))
    
    except APIHasChangedError as e:
      print(e)
      write_error(e)

    except Exception as e:
      print("error", e)
