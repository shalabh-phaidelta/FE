from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import asyncio

async def homepage(request):
    return JSONResponse({'message': 'Hello from Starlette!'})

async def background_task():
    await asyncio.sleep(5)
    print("Background task completed!")

async def start_background_task(request):
    asyncio.create_task(background_task())  # Runs in the background
    return JSONResponse({'message': 'Task started in the background'})

app = Starlette(
    debug=True,
    routes=[
        Route("/", homepage),
        Route("/run-task", start_background_task)
    ],
)
