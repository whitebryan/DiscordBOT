from WorldToBuildAPI import WorldTBAPI
import discord
from discord.ext import commands

keyFile = open("key.txt", "r")
key = keyFile.readline()

if len(key) > 0:
    intents = discord.Intents.all()
    apiClient = WorldTBAPI("!", intents)

    #read this from "key.txt" later
    apiClient.run(key)