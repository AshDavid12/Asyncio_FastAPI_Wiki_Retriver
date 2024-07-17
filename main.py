from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import uvicorn
import httpx
import asyncio

app = FastAPI()



state = {"first_paragraph": None}

class Article(BaseModel):
    name:str

@app.post("/articles/") #this is to accept an article name 
async def accept_article(article:Article): #create Article class instance called article
    return await get_first_par(article.name) #add AWAIT

@app.get("/articles/{article_name}")
async def get_first_par(article_name:str):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{article_name}" #from the wiki docs
    response = requests.get(url)
    data = response.json() #convert reponse to json object
    state["first_paragraph"] = data['extract'].split('\n')[0] 
    return {"article_name":article_name,"first_paragraph": state["first_paragraph"]}

@app.get("/")
def read_root():
        return {"message": f"Most recent article: {state['first_paragraph']}"}
