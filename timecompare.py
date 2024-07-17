import httpx
import asyncio
import time

N = 30  # Number of concurrent requests

async def fetch_url(client, url):
    start_time = time.perf_counter()
    response = await client.get(url)
    end_time = time.perf_counter()
    duration = end_time - start_time
    return response.status_code, duration

async def main_async(url):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [fetch_url(client, url) for url in urls]
        start_wall_time = time.perf_counter()
        responses = await asyncio.gather(*tasks)
        end_wall_time = time.perf_counter()

    total_wall_time = end_wall_time - start_wall_time
    print(f"Async total wall time: {total_wall_time:.4f} seconds")
    for i, (status, duration) in enumerate(responses):
        print(f"Request {i+1}: Status {status}, Time {duration:.4f} seconds")
    return total_wall_time

if __name__ == "__main__":
    #url = "https://en.wikipedia.org/wiki/dog"  # Replace with your target URL
    urls =["http://127.0.0.1:8000/articles/cat","http://127.0.0.1:8000/articles/dog","http://127.0.0.1:8000/articles/frog","http://127.0.0.1:8000/articles/human"]

    # Measure async version
    asyncio.run(main_async(urls))
