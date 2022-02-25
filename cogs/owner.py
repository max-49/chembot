import os
import json
import discord
import subprocess
import string
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='resetbot', help='resets all bot data')
    async def resetbot(self, ctx):
        await ctx.send("Resetting all saved data")
        await ctx.send("Data reset!")

    @commands.command(name='load', hidden=True, aliases=['l'])
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f"`{cog.split('.')[-1]}` cog successfully loaded!")

    @commands.command(name='unload', hidden=True, aliases=['u'])
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f"`{cog.split('.')[-1]}` cog successfully unloaded!")

    @commands.command(name='loadall', hidden=True)
    @commands.is_owner()
    async def loadall(self, ctx):
        for filename in os.listdir('cogs'):
            if filename.endswith('.py'):
                self.bot.load_extension(f'cogs.{filename[:-3]}')

    @commands.command(name='reload', aliases=['r'], hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f"`{cog.split('.')[-1]}` cog successfully reloaded!")

    @commands.command(name='updateprofiles', hidden=True)
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

    @commands.command(name='updatequestions', hidden=True)
    @commands.is_owner()
    async def updatequestions(self, ctx):
        with open('questions/categories.json') as j:
            categories = json.load(j)
        for category in categories:
            with open(f'questions/{category}.json') as j:
                questions = json.load(j)
            for question in questions:
                if(question['Calc'] == "True"):
                    question['Calc'] = True
                if(question['Table'] == "True"):
                    question['Table'] = True
                if(question['Calc'] == "False"):
                    question['Calc'] = False
                if(question['Table'] == "False"):
                    question['Table'] = False
            with open(f'questions/{category}.json', 'w') as j:
                questions = json.dump(questions, j)
        await ctx.send('Questions updated!')

    @commands.command(name='shell', hidden=True)
    @commands.is_owner()
    async def shell(self, ctx):
        await ctx.send('Shell spawned. Type `exit` to exit the shell.')
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower()[0] in string.printable

        while True:
            command = await self.bot.wait_for("message", check=check)
            print(f"$ {command.content}")
            if(command.content == 'exit'):
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
    @commands.command(name='fullrefresh', help='yo', aliases=['fr'], hidden=True)
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
        


    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")




def setup(bot):
    bot.add_cog(Owner(bot))
