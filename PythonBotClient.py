import discord
from discord import app_commands
from discord.ext import commands
from WorldToBuildAPI import WorldToBuildAPIClient, wtbRequestType

class PythonBotClient(discord.ext.commands.Bot):
    wtbAPIClient = WorldToBuildAPIClient()
    
    #Initalize as discord bot as well as set commands or listeners
    def __init__(self, command_prefix, clientIntents):
            super().__init__(command_prefix, intents=clientIntents)

            ##///////Commands///////##
            #Simple command that could be used for help with other commands
            @self.hybrid_command(name="serverhelp", description = "Get information about available commands", pass_context=True)
            async def serverHelp(ctx):
                if ctx.author != self.user:
                    await ctx.reply("There are currently no commands availible.")

            #Example for command only useable by certain roles
            @self.hybrid_command(name="roletest", description = "Test Admin ability", pass_context=True)
            async def adminAbility(ctx, name):
                roleNeeded = discord.utils.get(ctx.guild.roles, id=1119438872535896139)
                if roleNeeded in ctx.author.roles:
                    await ctx.reply("You have the correct role for this command")
                else:
                    await ctx.reply("You do not have the correct role for this command")

            ##Grab info from the World To Build API
            @self.hybrid_command(name="world_to_build_info", description = "Grab information about a player, club, or world", pass_context=True)
            async def getWTBInfo(ctx, type : wtbRequestType, id : app_commands.Range[int, 1]):
                """world_to_build_info
                Parameters
                -----------
                type: wtbRequestType
                    The type of information you are requesting
                id: int
                    The ID of the object you wish to get information about
                """                
                response = self.wtbAPIClient.getInfoByID(type, id)
                json = response.json()
                messageText = None
                newStatusText = None

                match type:
                    case wtbRequestType.Player:
                        if json["Success"] == False:
                            messageText = "Request failed please input a valid Player ID."
                        else:
                            messageText = f"The Player {json['Data']['Username']} was last online on {json['Data']['LastOnline']}"
                            newStatusText = f"Check out {json['Data']['Username']}!"
                    case wtbRequestType.Club:
                        if json["Success"] == False:
                            messageText = "Request failed please input a valid Club ID."
                        else:
                            messageText = f"The Club {json['Data']['Name']} is : \"{json['Data']['About']}\""
                            newStatusText = f"Check out {json['Data']['Name']}!"
                    case wtbRequestType.World:
                        if json["Success"] == False:
                            messageText = "Request failed please input a valid World ID."
                        else:
                            messageText = f"The World {json['Data']['Name']} is : \"{json['Data']['About']}\""
                            newStatusText = f"Check out {json['Data']['Name']}!"

                if newStatusText is not None:
                    await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=newStatusText))
                await ctx.reply(messageText)
            ##////////////////////##


            #Message listener
            @self.listen("on_message")
            async def on_message(message):
                if message.author == self.user:
                    return
                #Heres where you could add automod checking for words or links to bad places
            
            #Set to only be useable by my account atm, syncs commands so they show up as slash commands
            @self.command(name="SyncCommands", pass_context=True)
            async def syncBotCommands(ctx):
                if ctx.author.id == 161273263274590208:
                    await self.tree.sync()
                    print("Commands synced")

    #Command for when the bot is done loading
    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Unreal Engine"))

    #Called when any reaction is added
    #Here it is simply used to add a role if a user reacts with a certain emoji based off the emoji name
    async def on_raw_reaction_add(self, payload):
        role = None

        if payload.channel_id == 1119438630335828001:
            if payload.emoji.name == "filledHeart":
                role = discord.utils.get(payload.member.guild.roles, id=1119438872535896139)
            elif payload.emoji.name == "emprtHeart":
                role = discord.utils.get(payload.member.guild.roles, id=1119438912687972382)

            if role is not None and role not in payload.member.roles:
                await payload.member.send(f"You have received the {role.name} role.")
                await payload.member.add_roles(role)

    #Same as above but for recation removals 
    async def on_raw_reaction_remove(self, payload):
        role = None 

        guild = self.get_guild(payload.guild_id)
        member = discord.utils.get(guild.members, id=payload.user_id)

        if payload.channel_id == 1119438630335828001:
            if payload.emoji.name == "filledHeart":
                role = discord.utils.get(member.guild.roles, id=1119438872535896139)
            elif payload.emoji.name == "emprtHeart":
                role = discord.utils.get(member.guild.roles, id=1119438912687972382)

            if role is not None and role in member.roles:
                await member.send(f"You have lost the {role.name} role.")
                await member.remove_roles(role)
    


