import os
import platform

from itertools import cycle
from dotenv import load_dotenv

from sqlite3 import sqlite_version
from database import DB

import discord
from discord.ext import commands, tasks

def get_prefix(client, message):
	return DB.fetch_prefix(message.guild.id)

# Intents
intents = discord.Intents.default()
intents.members = True

# Client
client = commands.Bot(command_prefix=(get_prefix), intents=intents)
client.remove_command('help')

# Bot Variables
BOT_VERSION = "1.0.0"
BOT_LOG_CHANNEL = lambda: client.get_channel(908800710718652446)


STATUS = cycle(["default prefix *", "*help", "ig:@zewutz"])
@tasks.loop(seconds=7)
async def change_status():
    try:
        await client.change_presence(activity=discord.Game(next(STATUS)))
    except Exception as e:
        print(e)
        return

def cog_import():
	for file in os.listdir('./cogs'):
		if file.endswith(".py"):
			extension = file[:-3]
			try:
				client.load_extension(f"cogs.{extension}")
				print(f"[Cogs] '{extension} has been loaded.'")
			except Exception as e:
				print(e)
				exception = f"{type(e).__name__}: {e}"
				print(f"[Cogs] {extension} failed to load.\n{exception}")
				raise e

@client.event
async def on_ready():
    change_status.start()
    print('\nLogged in as {0.user}'.format(client))
    print(f'{client.user} is connected to {len(list(client.guilds))} servers.')
    print("------------------------------------")
    print(f'Current Bot version : {BOT_VERSION}')
    print(f"Sqlite3 version: {sqlite_version}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("\n")
    cog_import()


@client.event
async def on_guild_join(guild):
    guild_id = str(guild.id)
    guild_prefix = "*"

    DB.add_guild(guild_id, guild_prefix)

@client.event
async def on_guild_remove(guild):
    guild_id = str(guild.id)
    DB.delete_guild(guild_id)



def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await ctx.send(embed=embed)

        return
    if isinstance(error, commands.CommandNotFound):
        return
    await ctx.send(f"Error: {error}")

try:
    load_dotenv()
    client.run(os.getenv("TOKEN"))
except Exception as e:
    print(e)