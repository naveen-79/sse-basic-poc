import random
import json
from typing import Iterable

import asyncio
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_index():
    return FileResponse("index.html")


STREAM_DELAY = 2  # second
RETRY_TIMEOUT = 15000  # millisecond


def get_new_messages() -> Iterable:
    return [
        {
            "event": "new_message",
            "retry": RETRY_TIMEOUT,
            "data": json.dumps(
                {
                    "position": [
                        round(random.uniform(0.4, 8), 2),
                        round(random.uniform(0.4, 3), 2),
                        round(random.uniform(0.4, 8), 2),
                    ],
                }
            ),
        }
    ]


async def event_generator(request: Request):
    while True:
        if await request.is_disconnected():
            break
        for message in get_new_messages():
            yield message
        await asyncio.sleep(STREAM_DELAY)


@app.get("/stream")
async def message_stream(request: Request):
    return EventSourceResponse(event_generator(request))
