#!/usr/local/bin/python3

import asyncio
import websockets.server
from concurrent.futures import CancelledError

class Broadcast:
  def __init__(self):
    self.waiting = 0
    self.event = asyncio.Event()
    self.val = None
  def send(self, val):
    self.val = val
    self.event.set()
  async def recv(self):
    try:
      self.waiting += 1
      await self.event.wait()
      self.waiting -= 1
      if self.waiting == 0:
        self.event.clear()
      return self.val
    except CancelledError:
      self.waiting -= 1
      if self.waiting == 0:
        self.event.clear()

#CONNS = set()
NUM_CONNS = 0
TO_ALL_CONNS = Broadcast()

async def onRecv(text, conn_id):
  TO_ALL_CONNS.send(lambda cid: text)

async def handler(websocket, path):
  conn_id = NUM_CONNS
  NUM_CONNS += 1
  #CONNS.add(ws)
  try:
    while True:
      ws_listen_task = asyncio.ensure_future(websocket.recv())
      bc_listen_task = asyncio.ensure_future(TO_ALL_CONNS.recv())
      done, pending = await asyncio.wait(
        [ws_listen_task, bc_listen_task],
        return_when=asyncio.FIRST_COMPLETED)
      if ws_listen_task in done:
        text = ws_listen_task.result()
        await onRecv(text, conn_id)
      else:
        ws_listen_task.cancel()
      if bc_listen_task in done:
        get_text = bc_listen_task.result()
        await websocket.send(get_text(conn_id))
      else:
        bc_listen_task.cancel()
  finally:
    #CONNS.remove(ws)
    pass

start_serv = websockets.server.serve(handler, port=8765)
asyncio.get_event_loop().run_until_complete(start_serv)
asyncio.get_event_loop().run_forever()
