"""
Front-end interface API.
When ran it creates a websocket server on localhost port 4242. This websocket
feeds messages to the interface. Interface API is defined as JSON.
"""

import sys
import json
import asyncio
import websockets

from simulator.interface import Interface


DEFAULT_HOST_NAME = 'localhost'
DEFAULT_HOST_PORT = 4242


if __name__ == "__main__":

    isAlex = False # You're probably not Alex so we won't us sentry

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = DEFAULT_HOST_PORT

    if isAlex:
        from sentry.sentry import initialize_sentry
        client = initialize_sentry()

    try:

        interface = Interface()

        async def api_call(websocket, path):
            async for message in websocket:
                try:
                    msg = json.loads(message.replace("\\", "/"))
                    retMsg = interface.parse_command(msg)
                    rxStr = json.dumps(retMsg)
                    await websocket.send(rxStr)
                except Exception:
                    await websocket.send(json.dumps({
                        'status' : False,
                        'error' : 'cannot parse JSON message'
                    }))

        asyncio.get_event_loop().run_until_complete(
            websockets.serve(api_call, DEFAULT_HOST_NAME, port))
        asyncio.get_event_loop().run_forever()

    except Exception:
        if isAlex:
            client.captureException()
        else:
            print('Exception caught in main.py')
