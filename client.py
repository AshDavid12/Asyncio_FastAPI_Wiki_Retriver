import requests

BASE_URL = "http://127.0.0.1:8000"

def post_article(article_name):
    url = f"{BASE_URL}/articles/"
    response = requests.post(url, json={"name": article_name})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error posting article: {response.status_code} {response.text}")

def get_article(article_name):
    url = f"{BASE_URL}/articles/{article_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error getting article: {response.status_code} {response.text}")

if __name__ == "__main__":
    article_name = "Python_(programming_language)"  # Change this to any article name you want to fetch
    print("Posting article...")
    post_response = post_article(article_name)  # Sends article name to server
    print(f"Post response: {post_response}")

