from fastapi import APIRouter
from asyncio import Queue
from sse_starlette.sse import EventSourceResponse

message_queue = Queue()  # 全局消息队列，用于发送消息到客户端


# 在其他地方使用 send_message
async def send_message(message: str):
    await message_queue.put(message)


router = APIRouter(prefix='/sse', tags=["SSE"])


@router.get("/sse")
async def sse():
    # Register server side event
    async def event_generator():
        while True:
            message = await message_queue.get()
            yield {"data": message}

    return EventSourceResponse(event_generator())


@router.post("/send_message")
async def trigger_message(message: str):
    await send_message(message)
    return {"status": "Message sent"}


@router.get("/some_other_endpoint")
async def some_other_endpoint():
    # test send message from other place
    await send_message("Message from another endpoint")
    return {"status": "OK"}
