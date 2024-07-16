import requests

# Function to send a POST request to the /articles endpoint
def post_article(article_name):
    url = "http://127.0.0.1:8000/articles"
    payload = {"name": article_name}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("POST /articles response:", response.json())
    else:
        print(f"Failed to post article. Status code: {response.status_code}")

# Function to send a GET request to the root endpoint /
def get_latest_article():
    url = "http://127.0.0.1:8000/"
    response = requests.get(url)
    if response.status_code == 200:
        print("GET / response:", response.json())
    else:
        print(f"Failed to get latest article. Status code: {response.status_code}")



# Example for teminal you dont need this --- you can see results when trying in swagger and it also prints in the web server like that
#if __name__ == "__main__":
    # Post an article
    #post_article("dog")
    # Get the latest article
    #get_latest_article()
   
