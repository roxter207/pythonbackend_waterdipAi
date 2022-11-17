from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()

tasks = []


class CreateTask(BaseModel):
    title: str

class EditTask(BaseModel):
    title:str
    is_complete: bool


@app.post("/v1/tasks", status_code=201)
async def create_task(task: CreateTask):
    tasks.append(task)
    new_task = tasks[-1].dict()
    new_task.update({'id': len(tasks), "is_complete": False})
    tasks.pop()
    tasks.append(new_task)
    return_dict = {"id": new_task['id']}
    return return_dict


@app.get("/v1/tasks")
async def list_all_tasks():
    return tasks


@app.get("/v1/tasks/{task_id}")
async def get_single_task(task_id, response: Response):
    task = dict()
    for i in tasks:
        if (i['id']) == int(task_id):
            task = i
    
    if task == {}:
        response.status_code = 400
        return {"error": "There is no task at that id"}
    else:
        return task

@app.delete("/v1/tasks/{task_id}")
async def get_single_task(task_id, response: Response):
    task = dict()
    for i in tasks:
        if (i['id']) == int(task_id):
            tasks.remove(i)
            task = i
    
    if task == {}:
        response.status_code = 400
        return {"error": "There is no task at that id"}
    else:
        return task

@app.put("/v1/tasks/{task_id}" , status_code=204)
async def edit_task(task_id:int, task: EditTask, response:Response):
    for i in tasks:
        if (i['id']) == int(task_id):
            new_task = {'id': i['id'], 'title':task.title, "is_complete": task.is_complete}
            tasks.remove(i)
            tasks.append(new_task)
        else:
            new_task = {}
    if new_task == {}:
        response.status_code = 400
        return {"error": "There is no task at that id"}
    else:
        return

