# Laneo-Project
Automated QA agent utilizing browser-use and FastAPI.



## Installation
To run this application, you need to install the required dependencies. Run the following command: 
-> pip3 install fastapi uvicorn pydantic browser-use langchain_openai asyncio 
-> playwright install

## Running the Application
1. Open a terminal and navigate to the project directory.
2. Start the FastAPI server with:  uvicorn main:app --reload
3. The server will start locally at:  [http://127.0.0.1:8000]
4. Open the API documentation in your browser by running: [http://127.0.0.1:8000/docs]

## Using the API
### **Creating a Task** (POST `/tasks`)
1. In the Swagger UI (/docs), locate the POST /tasks endpoint.
2. Click on "Try it out".
3. Replace "string" in the request body with a description of what you want the agent to do.
4. Click "Execute" to send the request.
5. The response will have a task_id that you need to copy to retrieve the results with the get endpoint.

#### Example Input:
{
  "task_description": "I want you to go to the website (https://qacrmdemo.netlify.app/) and then define and run functional tests on the website using only the front-end. The identified bugs should be listed like this (EX. {Adding a new customer to the CRM})."
}


### Retrieving Task Results (GET /tasks/{task_id})
1. Locate the GET /tasks/{task_id} endpoint in /docs.
2. Click "Try it out", paste the task_id, and click "Execute".
3. The response will display the results once the agent completes the task.


## Understanding the Project

One thing to keep in mind when running this project is that the agent runs asynchronously. This means it takes some time to complete whatever task you’re giving it and actually return the results, so give it some time and pay attention to the terminal before assuming something is wrong with the code. Another issue I ran into was the agent getting stuck at "Step 1" (in my case, opening up the website https://qacrmdemo.netlify.app/). This basically means the agent is having trouble getting past the first step and is stuck in an infinite loop. I only recently started encountering this today and tested each part of my code independently (browser-use, FastAPI, Playwright) to confirm that browser-use was the issue. I haven’t found a solution to this error yet, but there is a page in the browser-use GitHub outlining possible fixes depending on which LLM model you're using (https://github.com/browser-use/browser-use/issues/839).
