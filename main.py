import aiohttp
import asyncio
import random
import sys
import os
from dotenv import load_dotenv
load_dotenv()

# Пример списка User-Agent строк
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
]

async def send_request(url, semaphore, index):
    user_agent = random.choice(USER_AGENTS)
    headers = {'User-Agent': user_agent}

    async with semaphore:
        conn = aiohttp.TCPConnector(limit_per_host=0)
        async with aiohttp.ClientSession(headers=headers, connector=conn) as session:
            try:
                async with session.get(url) as response:
                    status = response.status
                    await response.text()
                    print(f'Запрос {index} завершен с User-Agent: {user_agent}, Статус: {status}')
            except Exception as e:
                print(f'Ошибка при выполнении запроса {index}: {e}')

async def main():
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    tasks = []
    for i in range(NUM_TASKS):
        task = asyncio.create_task(send_request(REQUEST_URL, semaphore, i))
        tasks.append(task)
    await asyncio.gather(*tasks)

REQUEST_URL = os.getenv('REQUEST_URL')
NUM_TASKS = int(os.getenv('NUM_TASKS'))
CONCURRENCY_LIMIT = int(os.getenv('CONCURRENCY_LIMIT'))

if __name__ == '__main__':
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
