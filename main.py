from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import uvicorn

app = FastAPI()

state = {"first_paragraph": None}

class Article(BaseModel):
    name:str

@app.post("/articles/") #this is to accept an article name 
def accept_article(article:Article): #create Article class instance called article
    return get_first_par(article.name) #acsses artribute name 

@app.get("/articles/{article_name}")
def get_first_par(article_name:str):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{article_name}" #from the wiki docs
    response = requests.get(url) #make http request , the url is an endpoint of wiki api that provides the summery. 
    #it returns a response object that contains status,headers,body
    data = response.json() #convert reponse to json object
    state["first_paragraph"] = data['extract'].split('\n')[0] #we need to use split bc extract returns a summery. we want the first paragraph
    #so we split it at each new line that gives us a [] that has paraphraph as elements
    # then we take the first element using [0]
    return {"article_name":article_name,"first_paragraph": state["first_paragraph"]}


@app.get("/")
def read_root():
        return {"message": f"Most recent article: {state['first_paragraph']}"}
