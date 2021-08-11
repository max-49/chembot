import os
import discord
import chat_exporter
from discord.ext import commands
from discord_components import DiscordComponents
from discord.ext.commands import CommandNotFound

prefix = "c!"
intents = discord.Intents.default()
intents.members = True
help_command = commands.DefaultHelpCommand(no_category = 'Default')
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), help_command=help_command, intents=intents)
CHEM_TOKEN = os.getenv("CHEM_TOKEN")

if __name__ == '__main__':
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print("Setting NP game", flush=True)
    await bot.change_presence(activity=discord.Game(name="with cogs!!!!!!"))
    print(f'{bot.user.name} has connected to Discord!')
    DiscordComponents(bot)  
    chat_exporter.init_exporter(bot)

@bot.event
async def on_message(ctx):
    if ctx.content.startswith(prefix) and ctx.author.id != bot.user.id:
        print(f"{ctx.author.name}: {ctx.content}")
    await bot.process_commands(ctx)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        not_found = str(error).split('"')[1]
        await ctx.send(f"Command **`{not_found}`** not found.")
    # else:
    #     await ctx.send(f"**`ERROR:`** {type(error).__name__} - {error}")

bot.run(CHEM_TOKEN)