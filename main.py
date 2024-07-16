from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/wikipedia/{article_title}")
def get_wikipedia_first_paragraph(article_title: str):
    formatted_title = article_title.replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_title}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "extract" in data:
            first_paragraph = data["extract"]
            return {"article_title": article_title, "first_paragraph": first_paragraph}
        else:
            raise HTTPException(status_code=404, detail="Summary not available.")
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching article summary.")

# Run the server with: uvicorn your_script_name:app --reload
