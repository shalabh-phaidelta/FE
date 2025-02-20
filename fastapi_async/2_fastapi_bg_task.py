from fastapi import FastAPI, BackgroundTasks
import asyncio

app = FastAPI()

async def long_running_task():
    await asyncio.sleep(5)
    print("Background task completed!")

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/run-task")
async def run_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(long_running_task)
    return {"message": "Task started in the background!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
