import discord
from discord.ext import commands
from discord.ext.commands import Bot

from selenium import webdriver
from selenium.webdriver.common.by import By

from apikeys import *

class server:
  def __init__(self, servername, map, gamemode, playercount):
    self.servername = servername
    self.map = map
    self.gamemode = gamemode
    self.playercount = playercount

  def __key(self):
    return self.servername

  def __repr__(self):
    return "\nServer: % s \nMap: % s \nGamemode: % s \nPlayercount: % s" % (self.servername, self.map, self.gamemode, self.playercount)
  
  def __hash__(self):
    return hash(self.__key)

  def __eq__(self, other):
    return self.servername == other.servername
  
client = commands.Bot(command_prefix='!')

url = "https://bbspy.net/"
driver = webdriver.Edge()
driver.get(url)

@client.command()
async def hello(ctx):
  await ctx.send("Hello, I am Bot")

@client.command()
async def sandy(ctx):
  serverList = []
  
  driver.refresh()
  driver.implicitly_wait(2)
  servernames = driver.find_elements(By.XPATH, "//td[2]")
  maps = driver.find_elements(By.XPATH, "//td[3]")
  gamemodes = driver.find_elements(By.XPATH, "//td[5]")
  playercounts = driver.find_elements(By.XPATH, "//td[6]")

  for i in range(len(maps)):
    serverList.append(server(servernames[i].text, maps[i].text, gamemodes[i].text, playercounts[i].text, False))

  for i in reversed(range(len(serverList))):
    if serverList[i].map != "SandySunset":
      serverList.pop(i)
    elif serverList[i].gamemode != "CONQ" and serverList[i].gamemode != "INFCONQ" and serverList[i].gamemode != "FRONTLINE":
      serverList.pop(i)
    elif int(serverList[i].playercount.split('/')[0]) <= 128:
      serverList.pop(i)

  if (len(serverList) <= 0):
    await ctx.send("No good Sandy servers")
  else:
    for i in range(len(serverList)):
      await ctx.send(serverList[i])

@client.command()
async def zalfi(ctx):
  serverList = []
  
  driver.refresh()
  driver.implicitly_wait(2)
  servernames = driver.find_elements(By.XPATH, "//td[2]")
  maps = driver.find_elements(By.XPATH, "//td[3]")
  gamemodes = driver.find_elements(By.XPATH, "//td[5]")
  playercounts = driver.find_elements(By.XPATH, "//td[6]")

  for i in range(len(maps)):
    serverList.append(server(servernames[i].text, maps[i].text, gamemodes[i].text, playercounts[i].text, False))

  for i in reversed(range(len(serverList))):
    if serverList[i].map != "ZalfiBay":
      serverList.pop(i)
    elif serverList[i].gamemode != "CONQ" and serverList[i].gamemode != "INFCONQ":
      serverList.pop(i)
    elif int(serverList[i].playercount.split('/')[1]) <= 128 or int(serverList[i].playercount.split('/')[0]) <= 0:
      serverList.pop(i)

  if (len(serverList) <= 0):
    await ctx.send("No good Zalfi servers")
  else:
    for i in range(len(serverList)):
      await ctx.send(serverList[i])

client.run(token)
