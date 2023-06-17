from PythonBotClient import PythonBotClient
import discord
from discord.ext import commands

keyFile = open("key.txt", "r")
key = keyFile.readline()

#Checking for discord API key
if len(key) > 0:
    intents = discord.Intents.all()
    apiClient = PythonBotClient("!", intents)

    #read this from "key.txt" later
    apiClient.run(key)