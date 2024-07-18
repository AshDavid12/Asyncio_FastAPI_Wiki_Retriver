# Project 1 -Wiki FastAPI

Created by: Gaash David
Last edited: July 17, 2024 6:41 PM

# Asyncio FastAPI Wikipedia Retriever

### **Overview**

This project involves building a simple FastAPI server that uses asyncio to retrieve the first paragraph of a Wikipedia article given the name of the article. Students will learn the basics of asynchronous programming with asyncio and progressively refactor the server to be fully asynchronous using the httpx client.

### **Project Goals**

1. **Learn to use FastAPI to create web servers.**
2. **Understand asynchronous programming with asyncio.**
3. **Retrieve data from external APIs (Wikipedia).**
4. **Refactor synchronous code to be fully asynchronous.**

### **Technologies Used**

- **FastAPI**: For building the web server.
- **Asyncio**: For asynchronous programming in Python.
- **httpx**: For asynchronous HTTP requests.
- **requests**: For initial synchronous HTTP requests.
- **Python**: For implementing the server and clients.

### **Branch Explain** 
- redo branch: async version that uses a pre-existing httpx.AsyncClent created when server started
- step2 branch - async version with the client inside
- version1 branch - async version uses requests.get inside
- simple1 branch - doesnt include async  
#### **Files**:
- timecompare.py - a script to test the processing time across three versions (step2,version1,redo).
- client.py - invoke server

### **Project Workflow**

### **Step 1: Setting Up the FastAPI Server**

1. **Create a FastAPI Server**
    - Initialize a FastAPI project.
    - just used website- added fastapi in poetry and checked out examples.
    - Create a basic endpoint to accept article names.
    - Not post. Use @app.get
2. **Retrieve Wikipedia Articles (Synchronous)**
    - Implement an endpoint to fetch the first paragraph of a Wikipedia article using the requests library.
    - this is talking about the same endpoint as before. No need for two (post, get) only get.
    - wiki part:
        - you can find in the wiki documentation [https://en.wikipedia.org/api/rest_v1/#/Page content/get_page_summary__title_](https://en.wikipedia.org/api/rest_v1/#/Page%20content/get_page_summary__title_)
    
    | extract* | stringFirst several sentences of an article in plain text |
    | --- | --- |
    
    [/api/rest_v1/?spec](https://en.wikipedia.org/api/rest_v1/?spec) — then you find 
    
    page/summary/{article_title} - then extract 
    
    so construct url - `https://en.wikipedia.org/api/rest_v1/page/summary/{article_title}`
    
    basically just understand that extract is the key to the summery value in the dict. (later you need to split it for first paragraph).
    
    - the request library part: need to use requests.get(url) to get the response object.
    - Parse the response to extract the first paragraph.
    - to parse the response object returned by requests we need to convert it to dict.
    - Return the first paragraph as a JSON response.
    - once we converted we can return the first phragraph with using the extract key.
    - overview of the code:
    
    ```python
    response = requests.get(url) #contains server response to the get http request
    data = response.json() #json become a dict
    return {"first paragraph": data["extract"]}
    ```
    

1. **Test the Server**
- Test the server using CURL.

test post:

curl -X POST "[http://127.0.0.1:8000/articles](http://127.0.0.1:8000/articles)" -H "Content-Type: application/json" -d '{"name": "Python (programming language)"}'

test get:

curl -X GET "[http://127.0.0.1:8000/](http://127.0.0.1:8000/)"

(if you run after post then it will display the last one)

- Write a simple Python client using the requests library to invoke the server.
- basically seprate file to invoke server.
- the file contains also the requests.get(url)
- in the client py your url is the server link, in the main its the wikiapi thing
- in main for test you can run the post function in terminal
- you can also not have main and test it with the swagger
- this just pretends to be a client that uses the app. you run it with poetry run python client.py

### little helpful info for step1: 😎

- **`app.get`**:
    - Defines an endpoint in a FastAPI application.
    - Used on the server-side.
    - Specifies how the server should handle GET requests to a particular URL.
- **`requests.get`**:
    - Sends an HTTP GET request to a specified URL.
    - Used on the client-side.
    - Retrieves data from a web server or API.
- **Client Side**: Use HTTP methods to make requests to the server (e.g., using the `requests` library in Python).
- **Server Side**: Define how the server handles different HTTP methods (e.g., using FastAPI to define endpoints for GET, POST, PUT, DELETE, and PATCH requests).

### **Step 2: Refactor to Asynchronous Code**

1. **Implement Asynchronous Wikipedia Retrieval**
    - Replace the requests library with the httpx library for asynchronous HTTP requests.
    - Update the endpoint to use async/await syntax for the HTTP request.
2. **Handle Asynchronous Operations with asyncio**
    - Ensure all parts of the request handling are fully asynchronous.
    - Use asyncio features such as async functions and await.
- Notes all of the above:
    
    ```python
    #the syntax is simple just use 
    # async def getfunction
    async with httpx.AsyncClient(follow_redirects=True) as client:  # Enable follow REDIRECTS
           response = await client.get(url)  # Send a GET request to the Wikipedia API and await the response
    # everything else is the same
    ```
    
- Understand the idea:
    - async is not like multi threading. it is only used in python and its used for different functionality than multi threading. python has only one thread and async can be used for multi processing on multi cpus.
    - the idea here is that you're creating a async http client that will be used to make http request (such as get)
    - when we changed our request.get to await client. get, we’re enabling that if we’re stuck waiting for the request to complete the program will just execute something else in the meantime. this is the async part that is useful. so we’re not stuck waiting ever 🙂
- When using FastAPI, you don't need to manually manage the event loop with `asyncio.run` because FastAPI handles it for you.
1. **Test the Asynchronous Server**
    - Test the server using CURL to ensure it behaves as expected.
    - Update the Python client to use the httpx library for asynchronous requests and test the server.
    
    ```python
    #to update the client file
    BASE_URL = "http://127.0.0.1:8000"
    async def get_article(article_name):
        url = f"{BASE_URL}/articles/"
        async with httpx.AsyncClient(follow_redirects=True) as client: #similar syntax to the main.py
            response = await client.post(url, json={"name": article_name})
                return response.json()
           
    async def main():
        article_name = "snake"  # Change this to any article name you want to fetch
        print("Posting article...")
        post_response = await post_article(article_name)  # Sends article name to server
        print(f"Post response: {post_response}")
    
    if __name__ == "__main__":
        asyncio.run(main())
    ```
    

Tips: 

- remmebmer you can use the swagger to try out and execute from there

```python
# results wont show up on your web server unless you have this code
@app.get("/")
def read_root():
        return {"message": f"Most recent article: {state['first_paragraph']}"}
 #without this you can see it in terminal running curl or the client.py and on swagger 
 #but not on the server
```
