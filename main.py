import requests

def get_wikipedia_first_paragraph(article_title):
    # Replace spaces with underscores for the Wikipedia URL
    #formatted_title = article_title.replace(" ", "_")
    # Wikipedia API endpoint for article summary
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{article_title}"
    
    # Make the GET request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract the first paragraph (extract key)
        if "extract" in data:
            first_paragraph = data["extract"]
            return first_paragraph
        else:
            return "Summary not available."
    else:
        return f"Error: {response.status_code}"

# Example usage
article_title = "Dog"
first_paragraph = get_wikipedia_first_paragraph(article_title)
print(first_paragraph)
