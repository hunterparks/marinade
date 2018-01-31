#!/usr/bin/env python

import asyncio
import websockets

from sentry import initialize_sentry

sentry = initialize_sentry()

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message + ' ' + message)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 4242))
asyncio.get_event_loop().run_forever()
