import asyncio
async def task1():
    print("task 1 start")
    await asyncio.sleep(1)
    print("task 1 end")

async def task2():
    print("task 2 start")
    await asyncio.sleep(1)
    print("task 2 end")

async def task3():
    print("task 3 start")
    await asyncio.sleep(1)
    print("task 3 end")

async def main():
    await asyncio.gather(
        task1(),
        task2(),
        task3()
    )
asyncio.run(main())