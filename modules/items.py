import discord
from discord import activity
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game("Bot is online!"))
        print("It's online!")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')
