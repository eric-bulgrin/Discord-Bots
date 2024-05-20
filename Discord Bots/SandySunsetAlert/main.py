import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

from selenium import webdriver
from selenium.webdriver.common.by import By

from apikeys import *

class server:
  def __init__(self, servername, map, gamemode, playercount, newserver):
    self.servername = servername
    self.map = map
    self.gamemode = gamemode
    self.playercount = playercount
    self.newserver = newserver

  def __key(self):
    return self.servername

  def __repr__(self):
    return "\nServer: % s \nMap: % s \nGamemode: % s \nPlayercount: % s \nNewServer: % s" % (self.servername, self.map, self.gamemode, self.playercount, self.newserver)
  
  def __hash__(self):
    return hash(self.__key)

  def __eq__(self, other):
    return self.servername == other.servername

def getRefresh (oldList, driver):
  
  newList = []
  
  driver.refresh()
  driver.implicitly_wait(2)
  servernames = driver.find_elements(By.XPATH, "//td[2]")
  maps = driver.find_elements(By.XPATH, "//td[3]")
  gamemodes = driver.find_elements(By.XPATH, "//td[5]")
  playercounts = driver.find_elements(By.XPATH, "//td[6]")

  for i in range(len(maps)):
    newList.append(server(servernames[i].text, maps[i].text, gamemodes[i].text, playercounts[i].text, True))

  for i in reversed(range(len(newList))):
    if newList[i].map != "SandySunset":
      newList.pop(i)
    elif newList[i].gamemode != "CONQ" and newList[i].gamemode != "INFCONQ" and newList[i].gamemode != "FRONTLINE":
      newList.pop(i)
    elif int(newList[i].playercount.split('/')[0]) <= 128:
      newList.pop(i)

  finishedServers = [item for item in oldList if item not in newList]
  for item in finishedServers:
    oldList.remove(item)

  if len(oldList) > 0:
    for i in range(len(oldList)):
      oldList[i].newserver = False

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
    self.driver = webdriver.Edge()
    self.driver.get("https://bbspy.net/")

  async def setup_hook(self) -> None:
    self.my_background_task.start()

  async def on_ready(self):
    print(f'Logged in as {self.user} (ID: {self.user.id})')
    print('--------------------------------------------')

  @tasks.loop(seconds=10)
  async def my_background_task(self):
    channel = self.get_channel(int(channelId))

    self.masterList = getRefresh(self.masterList, self.driver)

    if len(self.masterList) > 0:
      for i in range(len(self.masterList)):
        if self.masterList[i].newserver == True:
          await channel.send(f'A New SandySunset Server Just Started:{self.masterList[i]}')

  @my_background_task.before_loop
  async def before_my_task(self):
    await self.wait_until_ready()

client = MyClient(intents=discord.Intents.default())

client.run(token)