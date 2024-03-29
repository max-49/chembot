import os
import sys
import pytz
import random
import discord
import platform
import chat_exporter
from config import get_bot
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import CommandNotFound

try:
    is_debug = sys.argv[1]
    if(is_debug.lower() == 'debug'):
        is_debug = True
    else:
        is_debug = False
except IndexError:
    is_debug = False
info = get_bot(os.getcwd().split('/')[-1], is_debug)

prefix = info[3]
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), help_command=None, intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False))

TOKEN = info[0]

@bot.event
async def on_ready():
    print("Setting NP game", flush=True)
    await bot.change_presence(activity=discord.Game(name=info[1]))
    print("Loading cogs")
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    if(is_debug):
        print("Running with level DEBUG")
    print("-------------------")

@bot.event
async def on_message(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        message = "DM: "
    else:
        message = ""
    if ctx.content.startswith(prefix) and ctx.author.id != bot.user.id:
        current_time = datetime.now(pytz.timezone('America/New_York')).strftime("%H:%M:%S")
        print(f"({current_time}) {message}{ctx.author.name}: {ctx.content}")
    if is_debug and ctx.author.id != 427832149173862400:
        return
    await bot.process_commands(ctx)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        not_found = str(error).split('"')[1]
        await ctx.send(f"Command **`{not_found}`** not found.")

bot.run(TOKEN)
