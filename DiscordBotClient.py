import discord
from discord import app_commands
from discord.ext import commands

class DiscordBotClient(discord.ext.commands.Bot):

    #Initalize as discord bot as well as set commands or listeners
    def __init__(self, command_prefix, clientIntents):
            super().__init__(command_prefix, intents=clientIntents)

            #Simple command that could be used for help with other commands
            @self.hybrid_command(name="serverhelp", pass_context=True)
            async def serverHelp(ctx):
                if ctx.author != self.user:
                    await ctx.channel.send("There are currently no commands availible.")

            #Example for command only useable by certain roles
            @self.hybrid_command(name="roletest", pass_context=True)
            async def adminAbility(ctx, name):
                roleNeeded = discord.utils.get(ctx.guild.roles, id=1119438872535896139)
                if roleNeeded in ctx.author.roles:
                    await ctx.channel.send("You have the correct role for this command")
                else:
                    await ctx.channel.send("You do not have the correct role for this command")

            #Message listener
            @self.listen("on_message")
            async def on_message(message):
                if message.author == self.user:
                    return

                if message.content.startswith('$Hello'):
                    await message.channel.send('Hello')
            
            #Set to only be useable by my account atm, syncs commands so they show up as slash commands
            @self.command(name="SyncCommands", pass_context=True)
            async def syncBotCommands(ctx):
                if ctx.author.id == 161273263274590208:
                    await self.tree.sync()
                    print("Commands synced")

    #Command for when the bot is done loading
    async def on_ready(self):
        print(f'We have logged in as {self.user}')

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
    


