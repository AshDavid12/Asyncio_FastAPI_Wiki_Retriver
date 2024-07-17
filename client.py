import requests
import httpx
import asyncio
BASE_URL = "http://127.0.0.1:8000"

async def post_article(article_name):
    url = f"{BASE_URL}/articles/"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.post(url, json={"name": article_name})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error posting article: {response.status_code} {response.text}")

async def get_article(article_name):
    url = f"{BASE_URL}/articles/"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.post(url, json={"name": article_name})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error posting article: {response.status_code} {response.text}")

async def main():
    article_name = "snake"  # Change this to any article name you want to fetch
    print("Posting article...")
    post_response = await post_article(article_name)  # Sends article name to server
    print(f"Post response: {post_response}")

if __name__ == "__main__":
    asyncio.run(main())
