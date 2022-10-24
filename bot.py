import asyncio
import discord
import config

from discord.ext import commands
from modules.items import Test
from modules.task_handler import TaskHandler

bot = commands.Bot(command_prefix=config.PREFIX, intents=discord.Intents.all())

async def setup():
    await bot.add_cog(Test(bot))
    await bot.add_cog(TaskHandler(bot))


if __name__ == '__main__':
    asyncio.run(setup())
    bot.run(config.TOKEN)