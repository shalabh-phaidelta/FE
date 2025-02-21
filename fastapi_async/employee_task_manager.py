from fastapi import FastAPI, BackgroundTasks
from nicegui import ui
import asyncio
import uvicorn
import requests
from threading import Thread

app = FastAPI()

# Dummy Employee Data
employees = [
    {"id": 1, "name": "Alice", "task": None},
    {"id": 2, "name": "Bob", "task": None},
    {"id": 3, "name": "Charlie", "task": None}
]
tasks = {}

async def complete_task(employee_id: int):
    """Simulate a long-running task"""
    await asyncio.sleep(5)
    tasks[employee_id] = "Completed"

@app.get("/employees")
async def get_employees():
    """Fetch employees"""
    return employees

@app.post("/assign-task/{employee_id}")
async def assign_task(employee_id: int, background_tasks: BackgroundTasks):
    """Assign a task to an employee"""
    employee = next((e for e in employees if e["id"] == employee_id), None)
    if not employee:
        return {"error": "Employee not found"}
    
    tasks[employee_id] = "In Progress"
    background_tasks.add_task(complete_task, employee_id)
    return {"message": f"Task assigned to {employee['name']}!"}

@app.get("/task-status/{employee_id}")
async def get_task_status(employee_id: int):
    """Check the task status"""
    return {"status": tasks.get(employee_id, "No Task Assigned")}

# ----------- NiceGUI UI -----------

def assign_task_ui():
    """Calls FastAPI to assign a task"""
    employee_id = slicer.value
    response = requests.post(f"http://127.0.0.1:8000/assign-task/{employee_id}")
    response_json = response.json()
    ui.notify(response_json.get("message", "Unexpected response from server"))

def check_status_ui():
    """Start polling task status for the selected employee"""
    employee_id = slicer.value

    def update_status():
        response = requests.get(f"http://127.0.0.1:8000/task-status/{employee_id}")
        status = response.json().get("status", "No Task Assigned")
        status_label.set_text(f"Task Status: {status}")

        # Stop polling once the task is completed
        if status == "Completed":
            polling_timer.deactivate()

    # Start the timer to check the status every 2 seconds
    global polling_timer
    polling_timer = ui.timer(2.0, update_status)


def start_gui():
    global slicer, status_label

    ui.label("Employee Task Manager").classes("text-xl font-bold")
    
    # Fetch employees dynamically
    try:
        employees_data = requests.get("http://127.0.0.1:8000/employees").json()
        employee_options = {e["id"]: e["name"] for e in employees_data}
    except Exception as e:
        employee_options = {}
        print(f"Error fetching employees: {e}")
    
    slicer = ui.select(employee_options, label="Select Employee").classes("w-64")
    ui.button("Assign Task", on_click=assign_task_ui).classes("mt-4 w-40")
    ui.button("Check Task Status", on_click=check_status_ui).classes("mt-2 w-40")
    
    status_label = ui.label("Task Status: No Task Assigned").classes("mt-4 text-lg")
    ui.run(port=8080)

if __name__ in {"__main__", "__mp_main__"}:
    # Run FastAPI in a separate thread
    Thread(target=lambda: uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")).start()
    start_gui()
