from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Global dictionary to store the latest article's first paragraph
state = {"first_paragraph": None}

# Define the data model for the article input
class ArticleInput(BaseModel):
    name: str

# POST endpoint to accept an article name
@app.post("/articles")
def receive_article(article: ArticleInput):
    formatted_title = article.name.replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_title}" #this is from the wikiapi doc
    
    response = requests.get(url) #from the HTTP GET request to wiki API store an instance of requests.Response class in reponse
    # this class has attributes like status code,text,content
    
    if response.status_code == 200: #sucsses request
        data = response.json() #convert to json
        if "extract" in data: #by the wiki api extact (key should be in json) is where the summery will be
            state["first_paragraph"] = data["extract"] #state is a dictionary so just put the summery as value in the dic under the firstpar key
            #article title is achived bc article is an instance of apydantic class articleinput. that has attribute name so .name 
            #works for acssessing 
            return {"message": "Article received", "article_title": article.name, "first_paragraph": state["first_paragraph"]}
        
        else:
            raise HTTPException(status_code=404, detail="Summary not available.")
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching article summary.")

# #GET endpoint to fetch the first paragraph of a Wikipedia article directly
# @app.get("/wikipedia/{article_title}")
# def get_wikipedia_first_paragraph(article_title: str):
#     formatted_title = article_title.replace(" ", "_")
#     url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_title}"
    
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         data = response.json()
#         if "extract" in data:
#             return {"article_title": article_title, "first_paragraph": data["extract"]}
#         else:
#             raise HTTPException(status_code=404, detail="Summary not available.")
#     else:
#         raise HTTPException(status_code=response.status_code, detail="Error fetching article summary.")




# BELOW- this is what prints it on the web server without it it will just be in the swagger
@app.get("/")
def read_root():
    if state["first_paragraph"]:
        return {"message": f"Most recent article: {state['first_paragraph']}"}
    else:
        return {"message": "No articles posted yet."}

# Run the server with: uvicorn your_script_name:app --reload
