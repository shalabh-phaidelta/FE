from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn
import asyncio

app = Starlette()

@app.route("/")
async def homepage(request):
    await asyncio.sleep(2)
    return JSONResponse({"message": "Hello, async world!"})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
