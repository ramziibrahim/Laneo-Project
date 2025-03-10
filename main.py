from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser
import asyncio
import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
browser = Browser()
tasks: Dict[str, Any] = {}



class TaskRequest(BaseModel):
    task_description: str

async def run_browser_use(task_id: str, task_description: str):
    try:
        agent = Agent(
            task=task_description,
            llm=ChatOpenAI(model="gpt-4o"),
            browser=browser,  
        )

        # Run the agent and get result
        result = await agent.run() 

        # Extract the result (i.e list of issues and descriptions)
        issues = []

        # List to store result
        issues = []

        if isinstance(result, str): #checks if result from agent is a string
            for line in result.split("\n"): # splits result into lines creating a list
                if " - " in line:  # checks if the line is valid (E.x of valid line {"Button Issue - Button is not clickable"})
                    issues.append(line)
        elif isinstance(result, dict) and "issues" in result: #check if the data returned is a dict and if there are even any issues
            issues = result["issues"]

        
        tasks[task_id] = {"status": "completed", "results": issues} #updates the specific task_id with the issues

    except Exception as e: #if agent fails, it will return failed status and the error
        tasks[task_id] = {"status": "failed", "error": str(e)} 


@app.post("/tasks")
async def create_task(request: TaskRequest):
    task_id = str(uuid.uuid4()) #generates unique id for the current task
    tasks[task_id] = {"status": "started"} #updates status to started
    asyncio.create_task(run_browser_use(task_id, request.task_description)) #makes call to run the actual agent
    return {"task_id": task_id}

@app.get("/tasks/{task_id}")
async def get_task_result(task_id: str): #takes in your specific task id
    return tasks.get(task_id, {"error": "Task not found or still in progress"})
