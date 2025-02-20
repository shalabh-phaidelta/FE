import asyncio

async def background_task():
    print("Background task: Start")
    await asyncio.sleep(5)
    print("Background task: Completed")

async def main():
    print("Main function: Start")
    asyncio.create_task(background_task())  # Background execution
    print("Main function: Doing other work...")
    await asyncio.sleep(2)
    print("Main function: End")

asyncio.run(main())
