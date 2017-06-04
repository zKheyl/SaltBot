import asyncio
import discord
from discord.ext.commands import Bot
import os
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy, StatSummaryType
from riotwatcher import RiotWatcher
from riotwatcher import EUROPE_WEST

#Initializing RiotWatcher
euw =  RiotWatcher('RGAPI-07f665c0-0784-4b4a-bc18-6790c273b626', default_region=EUROPE_WEST)



#Initializing Cassiopeia
riotapi.set_region("EUW")
riotapi.set_api_key("RGAPI-07f665c0-0784-4b4a-bc18-6790c273b626")
riotapi.set_load_policy(LoadPolicy.lazy)

#Bot Prefix
my_bot = Bot(command_prefix="!")

#this will go look into Riot API and return the KDA of the given player in params
@asyncio.coroutine
def GetKDA(player):
   summoner = riotapi.get_summoner_by_name(player)
   match_list = summoner.match_list()

   num_matches = 8

   kills = 0
   deaths = 0
   assists = 0

   for i, match_reference in enumerate(match_list[0:num_matches]):
       match = match_reference.match()
       for participant in match.participants:
           if participant.summoner_id == summoner.id:
               kills += participant.stats.kills
               deaths += participant.stats.deaths
               assists += participant.stats.assists
       kda = (kills + assists) / deaths

   return [kills,deaths,assists,kda]

#Checking into Riot API to see if players online or not
@asyncio.coroutine
def isInGame(player):
    summoner = riotapi.get_summoner_by_name(player)
    current_game = riotapi.get_current_game(summoner)
    if current_game is None:
        return False
    else:
        return True


@my_bot.event
async def on_read():
    print("Client logged in")

@asyncio.coroutine
def getServerStatus():
    if euw.get_server_status(region=EUROPE_WEST)['services'].pop(0)['status'] == "online":
        return True
    else:
        return False

#Checks if EUW is online
@my_bot.command()
async def server():
    loop = asyncio.get_event_loop()
    if loop.run_until_complete(getServerStatus) == True:
        return await my_bot.say("Le serveur EU WEST est en ligne!")
    else:
        return await my_bot.say("Le serveur EU WEST est down!")

#Check if player given in params is in a game atm
@my_bot.command()
async def inGame (_nom):
    loop = asyncio.get_event_loop()
    if loop.run_until_complete(inGame(_nom)):
        return await my_bot.say("Le joueur {0} est en game !".format(_nom))
    else:
        return await my_bot.say("Le joueur {0} n'est pas en game !".format(_nom))


#This is the Help function, the bot will display it in chat
@my_bot.command()
async def saltBot():
    await my_bot.say("!saltBot : affiche l'aide du bot")
    await my_bot.say("!kda player : affiche le Kda du joueur pass� en param�tre")
    await my_bot.say("!server : permet de savoir si le serveur europe est en ligne")
    return await my_bot.say("!inGame player : permet de savoir si le joueur est en game")

#Kda command
@my_bot.command()
async def kda(_nom):
    loop = asyncio.get_event_loop()
    await my_bot.say("Calcul du K/D/A...")
    loop.run_until_complete(kills,deaths,assists,kda = GetKDA(_nom))


    return await my_bot.say("Le joueur {0} a un  K/D/A de {1}/{2}/{3} = {4} sur les 20 derni�res parties".format(_nom,kills, deaths, assists, round(kda, 3)))



my_bot.run("MzE0Njc1NTUyMjM1ODE0OTEy.DBXygA.Q3BhBfkNGHofAkVAoLBk-i9IUms")
