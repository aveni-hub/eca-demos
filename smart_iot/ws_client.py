#!/usr/bin/env python3
"""websocket cmd client for wssrv.py example."""
import os
import argparse
import asyncio
import json
import signal
import aiohttp
from dotenv import load_dotenv

load_dotenv()

auth_key = os.getenv("AUTH_KEY")


async def start_client(url):
    headers = {
        "Authorization": "Bearer {}".format(auth_key)
    }
    # send request
    ws = await aiohttp.ClientSession().ws_connect(url, headers=headers, autoclose=False, autoping=False)

    async def dispatch():
        while True:
            msg = await ws.receive()
            if msg.type == aiohttp.WSMsgType.TEXT:
                print('Text: ', msg.data.strip())
            elif msg.type == aiohttp.WSMsgType.BINARY:
                print('Binary: ', msg.data)
            elif msg.type == aiohttp.WSMsgType.PING:
                await ws.pong()
            elif msg.type == aiohttp.WSMsgType.PONG:
                print('Pong received')
            else:
                if msg.type == aiohttp.WSMsgType.CLOSE:
                    await ws.close()
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print('Error during receive %s' % ws.exception())
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    pass

                break

    '''
    struct ModelReq {
        module_id: String,
        object: String,
        sync_rate: Dur,
        sync_once: bool,
        pretty: bool,
    }
    '''
    req = {
        "object": "ess",
        "module_id": "air_conditioner",
        "sync_once": False,
        "sync_rate": "1s",
        "pretty": False
    }
    req = json.dumps(req)
    await ws.send_str("/model {}".format(req))
    await dispatch()


ARGS = argparse.ArgumentParser(
    description="websocket console client for wssrv.py example.")
ARGS.add_argument(
    '--host', action="store", dest='host',
    default='127.0.0.1', help='Host name')
ARGS.add_argument(
    '--port', action="store", dest='port',
    default=2580, type=int, help='Port number')

if __name__ == '__main__':
    args = ARGS.parse_args()
    if ':' in args.host:
        args.host, port = args.host.split(':', 1)
        args.port = int(port)

    url = 'http://{}:{}/v1/ws'.format(args.host, args.port)

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, loop.stop)
    asyncio.Task(start_client(url))
    loop.run_forever()
