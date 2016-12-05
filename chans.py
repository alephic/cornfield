import asyncio
from concurrent.futures import CancelledError

class Channel:
  def __init__(self, loop=None):
    self.event = asyncio.Event(loop=loop)
    self.vals = []
  def send(self, val):
    self.vals.append(val)
    self.event.set()
  async def recv(self):
    try:
      await self.event.wait()
      result = self.vals.pop()
      if self.vals == []:
        self.event.clear()
      return result
    except CancelledError:
      pass

class Broadcaster:
  def __init__(self, loop=None):
    self.loop = loop
    self.subscribed = set()
  def send(self, val):
    for chan in self.subscribed:
      chan.send(val)
  def subscribe(self):
    chan = Channel(loop=self.loop)
    self.subscribed.add(chan)
    return chan
  def unsubscribe(self, chan):
    self.subscribed.remove(chan)
