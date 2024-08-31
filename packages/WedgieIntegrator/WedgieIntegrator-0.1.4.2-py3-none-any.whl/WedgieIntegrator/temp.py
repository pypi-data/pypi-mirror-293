from asyncio_workaround import run

async def print_something(msg):
    print(msg)


run(print_something("hi"))
