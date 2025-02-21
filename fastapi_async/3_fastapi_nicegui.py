from fastapi import FastAPI, BackgroundTasks
from nicegui import ui
import asyncio
import uvicorn
import requests
from threading import Thread
import time

app = FastAPI()

async def long_running_task():
    await asyncio.sleep(5)
    print("Background task completed!")

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI with NiceGUI!"}

@app.get("/run-task")
async def run_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(long_running_task)
    return {"message": "Task started in the background!"}

def run_task_ui():
    """ Calls the FastAPI endpoint when button is clicked """
    response = requests.get("http://127.0.0.1:8000/run-task")
    ui.notify(response.json()["message"])  # Notify user in UI

def start_gui():
    ui.label("FastAPI + NiceGUI Example")
    ui.button("Run Task", on_click=run_task_ui)
    ui.run(port=8080)  # Ensure NiceGUI starts properly

if __name__ in {"__main__", "__mp_main__"}:
    # Run FastAPI in a separate thread
    thread = Thread(target=lambda: uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info"), daemon=True)
    thread.start()

    time.sleep(2)  # Ensure FastAPI is up before UI starts
    start_gui()
