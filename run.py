import discord
from discord.ext import commands
from config import config
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config.BOT_PREFIX,intents=intents)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"Synced {synced} commands")
    print(f"Log in with --> {bot.user}")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.tree.command()
async def reload(interaction: discord.Interaction):
    await interaction.response.defer()
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.unload_extension(f"cogs.{filename[:-3]}")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
    synced = await bot.tree.sync()
    print(f"Synced {synced} commands")
    await interaction.followup.send("reload successfully.", ephemeral = True)

if __name__ == "__main__":
    asyncio.run(load_extensions())
    bot.run(config.BOT_TOKEN)