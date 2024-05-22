import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

import requests
from requests.auth import HTTPDigestAuth
import json

from apikeys import *

import logging

logging.basicConfig(filename='logs.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class server:
  def __init__(self, servername, servermap, gamemode, playercount, maxplayers, newserver):
    self.servername = servername
    self.servermap = servermap
    self.gamemode = gamemode
    self.playercount = playercount
    self.maxplayers = maxplayers
    self.newserver = newserver

  def __key(self):
    return self.servername

  def __repr__(self):
    return "\nServer: % s \nMap: % s \nGamemode: % s \nPlayercount: % s \nMaxPlayers: % s" % (self.servername, self.servermap, self.gamemode, self.playercount, self.maxplayers)
  
  def __hash__(self):
    return hash(self.__key)

  def __eq__(self, other):
    return self.servername == other.servername

def getApiResponse(oldList):
  newList = []

  if len(oldList) > 0:
    for i in range(len(oldList)):
      oldList[i].newserver = False

  url = "https://publicapi.battlebit.cloud/Servers/GetServerList"
  myResponse = requests.get(url)

  if (myResponse.ok):
    jData = json.loads(myResponse.content)
    
    for item in jData:
      newList.append(server(item["Name"], item["Map"], item["Gamemode"], item["Players"], item["MaxPlayers"], True))
  else:
    logging.info('API status code was %s, not 200', myResponse.status_code)
    return oldList

  for i in reversed(range(len(newList))):
    if newList[i].servermap != "SandySunset":
      newList.pop(i)
    elif newList[i].gamemode != "CONQ" and newList[i].gamemode != "INFCONQ" and newList[i].gamemode != "FRONTLINE":
      newList.pop(i)
    elif newList[i].playercount <= 128:
      newList.pop(i)

  finishedServers = [item for item in oldList if item not in newList]
  for item in finishedServers:
    oldList.remove(item)

  for item1 in oldList:
    for item2 in newList:
      if item1 == item2:
        newList.remove(item2)

  for item in newList:
    oldList.append(item)

  return oldList

class MyClient(discord.Client):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.masterList = []

  async def setup_hook(self) -> None:
    self.my_background_task.start()

  async def on_ready(self):
    logging.info(f'Logged in as {self.user} (ID: {self.user.id})')
    logging.info('--------------------------------------------')

  @tasks.loop(seconds=5)
  async def my_background_task(self):
    channel = self.get_channel(int(channelId))
    
    self.masterList = getApiResponse(self.masterList)

    if len(self.masterList) > 0:
      for i in range(len(self.masterList)):
        if self.masterList[i].newserver == True:
          logging.info(f'A New SandySunset Server Just Started:{self.masterList[i]}')
          await channel.send(f'A New SandySunset Server Just Started:{self.masterList[i]}')

  @my_background_task.before_loop
  async def before_my_task(self):
    await self.wait_until_ready()

client = MyClient(intents=discord.Intents.default())

client.run(token)
