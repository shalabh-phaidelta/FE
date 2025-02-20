import asyncio

async def task_a():
    print("Task A: Start")
    await asyncio.sleep(3)
    print("Task A: End")

async def task_b():
    print("Task B: Start")
    await asyncio.sleep(1)
    print("Task B: End")

async def main():
    print("Main: Start")
    await asyncio.gather(task_a(), task_b())
    print("Main: End")

asyncio.run(main())
