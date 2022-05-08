import os
import json
import discord
import subprocess
import string
from config import get_bot
from discord.ext import commands
from discord.ext.commands import BadArgument, MissingRequiredArgument


class Owner(commands.Cog):
    def __init__(self, bot):
        self.info = get_bot(os.getcwd().split('/')[-1])
        self.bot = bot

    @commands.command(name='load', help='load a cog', aliases=['l'], usage="load <cog>")
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f"`{cog.split('.')[-1]}` cog successfully loaded!")

    @commands.command(name='unload', help='unload a cog', aliases=['u'], usage="unload <cog>")
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f"`{cog.split('.')[-1]}` cog successfully unloaded!")

    @commands.command(name='loadall', help='load all cogs', usage="loadall")
    @commands.is_owner()
    async def loadall(self, ctx):
        for filename in os.listdir('cogs'):
            if filename.endswith('.py'):
                self.bot.load_extension(f'cogs.{filename[:-3]}')

    @commands.command(name='reload', help='reload a cog', aliases=['r'], usage="reload <cog>")
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f"`{cog.split('.')[-1]}` cog successfully reloaded!")

    @commands.command(name='reloadall', help='reload all cogs', aliases=['ra'], usage="reloadall")
    @commands.is_owner()
    async def reloadall(self, ctx):
        for filename in os.listdir('cogs'):
            if filename.endswith('.py'):
                try:
                    self.bot.unload_extension(f'cogs.{filename[:-3]}')
                    self.bot.load_extension(f'cogs.{filename[:-3]}')
                except Exception as e:
                    await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        await ctx.send("All cogs successfully reloaded!")

    @commands.command(name='updateprofiles', hidden=True, usage="updateprofiles")
    @commands.is_owner()
    async def updateprofiles(self, ctx):
        with open('profiles.json') as j:
            profile_data = json.load(j)
        for i in range(len(profile_data)):
            if(profile_data[i]['Balance'] < 0):
                profile_data[i]['Balance'] = 0
            if(profile_data[i]['Balance'] > 20000):
                profile_data[i]['Balance'] = 20000
            profile_data[i]['WordleWins'] = 0
            profile_data[i]['WordleTotal'] = 0
            profile_data[i]['didDaily'] = False
        with open('profiles.json', 'w') as j:
            json.dump(profile_data, j)
        await ctx.send("Profiles updated!")

    @commands.command(name='shell', help="spawns a shell from the vps to execute commands in", usage="shell")
    @commands.is_owner()
    async def shell(self, ctx):
        await ctx.send('Shell spawned. Type `exit` to exit the shell.')
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower()[0] in string.printable

        while True:
            command = await self.bot.wait_for("message", check=check)
            print(f"$ {command.content}")
            if(command.content.lower() == 'exit'):
                break
            try:
                proc = subprocess.check_output([command.content], shell=True).decode("utf-8")
            except subprocess.CalledProcessError as e:
                proc = e.stdout
            if(proc == b""):
                await ctx.send("Command errored but idk how to get the error message to show")
            else:
                if(proc != ""):
                    await ctx.send(f"```{proc}```")
                else:
                    await ctx.send("Command executed with no stdout")
        
        await ctx.send('Shell exited')

    @commands.is_owner()
    @commands.command(name='fullrefresh', help='pull latest changes from the GitHub and reload a cog', aliases=['fr'], usage="fullrefresh <cog>")
    async def fullrefresh(self, ctx, cog: str):
        command = "git pull --no-edit"
        try:
            proc = subprocess.check_output([command], shell=True).decode("utf-8")
        except subprocess.CalledProcessError as e:
            proc = e.stdout
        await ctx.send(f"```{proc}```")
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f"`{cog.split('.')[-1]}` cog successfully reloaded!")

    @commands.is_owner()
    @commands.command(name='fullrefreshall', help='pull latest changes from GitHub and reload all commands', aliases=['fra'], usage="fullrefreshall")
    async def fullrefreshall(self, ctx):
        command = "git pull --no-edit"
        try:
            proc = subprocess.check_output([command], shell=True).decode("utf-8")
        except subprocess.CalledProcessError as e:
            proc = e.stdout
        await ctx.send(f"```{proc}```")
        await ctx.invoke(self.bot.get_command('reloadall'))

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument) or isinstance(error, BadArgument):
            await ctx.reply(f"Incorrect syntax! Command usage: {self.info[3]}{ctx.command.usage}")
        else:
            await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")





def setup(bot):
    bot.add_cog(Owner(bot))
