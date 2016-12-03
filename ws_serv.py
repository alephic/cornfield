
import asyncio
import websockets

connections = set()

async def handler(ws, path):
  connections.add(ws)
  try:
    while True:
      listener_task = asyncio.ensure_future(ws.recv())
      #TODO replace producer()
      producer_task = asyncio.ensure_future(producer())
      done, pending = await asyncio.wait(
        [listener_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED)
      if listener_task in done:
        msg = listener_task.result()
        await consumer(msg)
        #TODO replace consumer(msg)
      else:
        listener_task.cancel()
      if producer_task in done:
        msg = producer_task.result()
        await ws.send(msg)
      else:
        producer_task.cancel()
  finally:
    connections.remove(ws)

start_serv = websockets.serve(hello, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_serv)
asyncio.get_event_loop().run_forever()
