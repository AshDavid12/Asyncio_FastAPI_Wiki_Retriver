from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

# Global dictionary to store the latest article's first paragraph
state = {"first_paragraph": None}

# Define the data model for the article input
class ArticleInput(BaseModel):
    name: str

# POST endpoint to accept an article name
@app.post("/articles")
async def receive_article(article: ArticleInput):
    return await get_wikipedia_first_paragraph(article.name) #add AWAIT

# GET endpoint to fetch the first paragraph of a Wikipedia article directly
@app.get("/wikipedia/{article_title}")
async def get_wikipedia_first_paragraph(article_title: str):
    formatted_title = article_title.replace(" ", "_")  # Replace spaces with underscores for the Wikipedia URL
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_title}"  # Construct the URL for the Wikipedia API

    async with httpx.AsyncClient(follow_redirects=True) as client:  # Enable follow REDIRECTS
        try:
            response = await client.get(url)  # Send a GET request to the Wikipedia API and await the response
        except httpx.RequestError as exc:
            # Handle any request exceptions (e.g., network issues)
            raise HTTPException(status_code=500, detail=f"An error occurred while requesting {exc.request.url!r}.") from exc

    if response.status_code == 200:  # Check if the response status code is 200 (OK)
        try:
            data = response.json()  # Parse the response JSON content
        except ValueError:
            # Handle JSON parsing errors
            raise HTTPException(status_code=500, detail="Error parsing response from Wikipedia API.")
        
        if "extract" in data:  # Check if the "extract" key is present in the response data
            return {"article_title": article_title, "first_paragraph": data["extract"]}  # Return a JSON response with the article title and first paragraph
        else:
            raise HTTPException(status_code=404, detail="Summary not available.")  # Raise a 404 error if the summary is not available
    else:
        # Log detailed error information
        raise HTTPException(status_code=response.status_code, detail=f"Error fetching article summary. Status code: {response.status_code}, Response: {response.text}")

# Root endpoint to display the latest stored article's first paragraph
@app.get("/")
async def read_root():
    if state["first_paragraph"]:  # Check if there is a stored first paragraph in the global state
        return {"message": f"Most recent article: {state['first_paragraph']}"}  # Return the most recent article's first paragraph
    else:
        return {"message": "No articles posted yet."}  # Return a message indicating no articles have been posted
