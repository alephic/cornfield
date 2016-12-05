#!/usr/local/bin/python3

import asyncio
import websockets.server
from websockets.exceptions import ConnectionClosed
from chans import *

NUM_CONNS = 0
TO_ALL_CONNS = Broadcaster(loop=asyncio.get_event_loop())

def onRecv(text, conn_id):
  global TO_ALL_CONNS
  print('Received from conn #'+str(conn_id)+': "'+text+'"')
  TO_ALL_CONNS.send(lambda cid: text)

async def handler(websocket, path):
  global NUM_CONNS
  global TO_ALL_CONNS
  from_all = TO_ALL_CONNS.subscribe()
  conn_id = NUM_CONNS
  NUM_CONNS += 1
  print('Established connection #'+str(conn_id))
  try:
    while True:
      ws_listen_task = asyncio.ensure_future(websocket.recv())
      bc_listen_task = asyncio.ensure_future(from_all.recv())
      done, pending = await asyncio.wait(
        [ws_listen_task, bc_listen_task],
        return_when=asyncio.FIRST_COMPLETED)
      if ws_listen_task in done:
        text = ws_listen_task.result()
        onRecv(text, conn_id)
      else:
        ws_listen_task.cancel()
      if bc_listen_task in done:
        get_text = bc_listen_task.result()
        text = get_text(conn_id)
        print('Sending to conn #'+str(conn_id)+': "'+text+'"')
        await websocket.send(text)
      else:
        bc_listen_task.cancel()
  except ConnectionClosed:
    pass
  finally:
    TO_ALL_CONNS.unsubscribe(from_all)
    pass

start_serv = websockets.server.serve(handler, port=8765)
asyncio.get_event_loop().run_until_complete(start_serv)
asyncio.get_event_loop().run_forever()
