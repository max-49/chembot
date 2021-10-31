import os
import sys
import discord
import platform
import chat_exporter
from config import get_bot
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
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), help_command=None, intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False))

TOKEN = info[0]

if __name__ == '__main__':
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    print("Setting NP game", flush=True)
    await bot.change_presence(activity=discord.Game(name=info[1]))
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    if(is_debug):
        print("Running with level DEBUG")
    print("-------------------")
    chat_exporter.init_exporter(bot)


@bot.event
async def on_message(ctx):
    if ctx.content.startswith(prefix) and ctx.author.id != bot.user.id:
        print(f"{ctx.author.name}: {ctx.content}")
    if ctx.author.id == 523309470105993226:
        await ctx.channel.send('based opinion sean I agree')
    if is_debug and ctx.author.id != 427832149173862400:
        return
    await bot.process_commands(ctx)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        not_found = str(error).split('"')[1]
        await ctx.send(f"Command **`{not_found}`** not found.")

bot.run(TOKEN)
