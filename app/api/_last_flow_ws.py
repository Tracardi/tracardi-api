import asyncio
import json

import aioredis
from fastapi import APIRouter, Depends
from websockets.exceptions import ConnectionClosedOK

from app.api.auth.permissions import Permissions
from typing import Optional
from fastapi import WebSocket, WebSocketDisconnect

from tracardi.config import redis_config
from tracardi.service.storage.redis_client import RedisClient

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "maintainer"]))]
)


class ConnectionManager:
    def __init__(self):
        self.active_connection: Optional[WebSocket] = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connection = websocket

    async def disconnect(self, websocket: WebSocket):
        self.active_connection = None

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    # async def broadcast(self, message: str):
    #     for connection in self.active_connections:
    #         await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        data = 1

        while True:
            rec = await websocket.receive_text()
            if rec == 'stop':
                break
            print(data)
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            data += 1
            await asyncio.sleep(1)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        # await manager.broadcast(f"Client #{client_id} left the chat")
    except ConnectionClosedOK:
        print('closed ', client_id)


@router.websocket("/redis/{client_id}")
async def websocket_endpoint_redis(websocket: WebSocket):
    await websocket.accept()

    redis = RedisClient()
    psub = redis.pubsub()
    with psub as p:
        print(await p.subscribe("channel:1"))
    print(redis)
    # ------------------ SEND SUBSCRIBE RESULT THROUGH WEBSOCKET ----------------- #
    # (channel,) = await redis.client.subscribe("tracardi:queue")
    # try:
    #     while True:
    #         response_raw = await channel.get()
    #         response_str = response_raw.decode("utf-8")
    #         response = json.loads(response_str)
    #
    #         if response:
    #             await websocket.send_json({
    #                 "event": 'NEW_CHECK_RESULT',
    #                 "data": response
    #             })
    # except WebSocketDisconnect as e:
    #     raise e
