#!/usr/local/bin/python3

import asyncio
import websockets.server
from websockets.exceptions import ConnectionClosed
from concurrent.futures import CancelledError

class Broadcast:
  def __init__(self, loop=None):
    self.waiting = 0
    self.event = asyncio.Event(loop=loop)
    self.val = None
  def send(self, val):
    self.val = val
    self.event.set()
    print("event set")
  async def recv(self):
    try:
      self.waiting += 1
      await self.event.wait()
      print("wait over")
      self.waiting -= 1
      if self.waiting == 0:
        self.event.clear()
      return self.val
    except CancelledError:
      print("wait cancelled")
      self.waiting -= 1
      if self.waiting == 0:
        self.event.clear()

#CONNS = set()
NUM_CONNS = 0
TO_ALL_CONNS = Broadcast(loop=asyncio.get_event_loop())

async def onRecv(text, conn_id):
  global TO_ALL_CONNS
  print('Received from conn #'+str(conn_id)+': "'+text+'"')
  TO_ALL_CONNS.send(lambda cid: text)

async def handler(websocket, path):
  global NUM_CONNS
  global TO_ALL_CONNS
  conn_id = NUM_CONNS
  NUM_CONNS += 1
  print('Established connection #'+str(conn_id))
  #CONNS.add(websocket)
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
        text = get_text(conn_id)
        print('Sending to conn #'+str(conn_id)+': "'+text+'"')
        await websocket.send(text)
      else:
        bc_listen_task.cancel()
  except ConnectionClosed:
    pass
  finally:
    #CONNS.remove(websocket)
    pass

start_serv = websockets.server.serve(handler, port=8765)
asyncio.get_event_loop().run_until_complete(start_serv)
asyncio.get_event_loop().run_forever()
