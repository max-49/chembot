import os
import json
import random
import string
import discord
import asyncio
from discord.ext import commands
from datetime import datetime

class Spaces(discord.ui.View):
    def __init__(self, word: str, guesses=None, exitt=None):
        super().__init__()
        word = word.upper()
        self.value = True
        if (exitt):
            for child in self.children:
                child.disabled = True
            self.value = False
        elif (guesses):
            for j, guess in enumerate(guesses):
                guess = guess.upper()
                for i, (x,y) in enumerate(zip(guess, word)):
                    self.children[i + 5 * j].label = x
                    if x == y:
                        self.children[i + 5 * j].style = discord.ButtonStyle.green
                    elif y in guess and self.children[i + 5 * j].style != discord.ButtonStyle.green:
                        indices = [i for i, c in enumerate(guess) if c == y]
                        for index in indices:
                            if self.children[index + 5 * j].style != discord.ButtonStyle.green:
                                self.children[index + 5 * j].style = discord.ButtonStyle.blurple
                if guess == word:
                    for child in self.children:
                        child.disabled = True
                    self.value = False
                
 
    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def a(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def b(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def c(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0
    
    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def d(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def e(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def f(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def g(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def h(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def i(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def j(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def k(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0
    
    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def l(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def m(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def n(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def o(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def p(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def q(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def r(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def s(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def t(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def u(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def v(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def w(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def x(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def y(self, button: discord.ui.Button, interaction: discord.Interaction):
        filler = 0

class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wordle", help="world")
    async def wordle(self, ctx):
        with open(f'profiles.json') as f:
            profile_data = json.load(f)
        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and msg.content.lower()[0] in string.printable
        words = []
        doingDaily = True
        with open('words.txt') as j:
            for line in j.readlines():
                words.append(line.strip())
        # if doingDaily:
        #     date = datetime.now().date()
        #     word = words[int(((date.year * date.day) / date.month) % len(words))]
        # else:
        word = random.choice(words)
        with open('words_also.txt') as j:
            for line in j.readlines():
                words.append(line.strip())
        game = Spaces(word)
        embed = discord.Embed(title="Wordle")
        view = await ctx.send(embed=embed, view=game)
        guess_number = 0
        guesses = []
        while guess_number < 5:
            if(not game.value):
                embed=discord.Embed(title="You win!", color=0x00FF00)
                if(doingDaily):
                    for i in range(len(profile_data)):
                        if(profile_data[i]['ID'] == ctx.author.id):
                            profile_data[i]['WordleWins'] = profile_data[i]['WordleWins'] + 1
                            profile_data[i]['WordleTotal'] = profile_data[i]['WordleTotal'] + 1 
                            profile_data[i]['didDaily'] = True
                    with open('profiles.json', 'w') as j:
                        json.dump(profile_data, j)
                return await view.edit(embed=embed, view=game)
            guess = await self.bot.wait_for("message", check=check)
            if guess.content.lower() == 'exit' or guess.content.lower() == 'quit':
                game = Spaces(word, guesses, 'exit')
                await ctx.send("Quitting game...")
                return await view.edit(embed=embed, view=game)
            if len(guess.content) < 5:
                await guess.add_reaction('❌')
                embed = discord.Embed(title="Too Short! Guess again.")
                await view.edit(embed=embed, view=game)
                continue
            elif len(guess.content) > 5:
                await guess.add_reaction('❌')
                embed = discord.Embed(title="Too Long! Guess again.")
                await view.edit(embed=embed, view=game)
                continue
            elif guess.content not in words:
                await guess.add_reaction('❌')
                embed = discord.Embed(title="Word not in wordlist! Guess again.")
                await view.edit(embed=embed, view=game)
                continue
            else:
                guesses.append(guess.content.lower())
                embed = discord.Embed(title="Wordle")
                game = Spaces(word, guesses)
                await view.edit(embed=embed, view=game)
                guess_number += 1
        if(not game.value):
            embed=discord.Embed(title="You win!", color=0x00FF00)
            if(doingDaily):
                for i in range(len(profile_data)):
                    if(profile_data[i]['ID'] == ctx.author.id):
                        profile_data[i]['WordleWins'] = profile_data[i]['WordleWins'] + 1
                        profile_data[i]['WordleTotal'] = profile_data[i]['WordleTotal'] + 1 
                        profile_data[i]['didDaily'] = True
                with open('profiles.json', 'w') as j:
                    json.dump(profile_data, j)
            return await view.edit(embed=embed, view=game)
        else:
            embed = discord.Embed(title="You lose... Better luck next time!", description=f"The word was {word}", color=0xFF0000)
            if(doingDaily):
                for i in range(len(profile_data)):
                    if(profile_data[i]['ID'] == ctx.author.id):
                        profile_data[i]['WordleTotal'] = profile_data[i]['WordleTotal'] + 1 
                        profile_data[i]['didDaily'] = True
                with open('profiles.json', 'w') as j:
                    json.dump(profile_data, j)
            await view.edit(embed=embed, view=game)
        
    @commands.command(name="wordlestats", help="wordle stats")
    async def wordlestats(self, ctx, profile: discord.Member=None):
        with open(f'profiles.json') as f:
            profile_data = json.load(f)
        
        uid = ctx.author.id if profile is None else profile.id
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == uid):
                embedVar = discord.Embed(
                    title=f"{profile_data[i]['Name']}'s profile",  timestamp=datetime.utcnow(), color=0x00ff00)
                try:
                    percent_correct = (profile_data[i]['WordleWins']/profile_data[i]['WordleTotal']) * 100
                except ZeroDivisionError:
                    percent_correct = 0
                embedVar.add_field(name="Wordle Stats", value=f"{str(profile_data[i]['WordleWins'])}/{str(profile_data[i]['WordleTotal'])} ({str(round(percent_correct, 2))}%)", inline=False)
                embedVar.set_thumbnail(url=profile_data[i]['Avatar URL'])
                await ctx.send(embed=embedVar)
                return
        else:
            if profile is None:
                profile = ctx.author
            profile_data.append({"Name": profile.name, "Tag": str(profile), "Nick": profile.display_name, "ID": profile.id, "Avatar URL": str(profile.avatar.url), "Correct": 0, "Total": 0, "Calc": "True", "Table": "True", "WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1, "Times": 0, "Win": 0, "Lose": 0, "Profit": 0, "WordleWins": 0, "WordleTotal": 0, "didDaily": False})
            embedVar = discord.Embed(title=f"{profile.name}'s profile",  timestamp=datetime.utcnow(), color=0x00ff00)
            percent_correct = 0
            embedVar.add_field(name="Profile initialized!", value="Run the command again to see your profile!", inline=False)
            embedVar.set_thumbnail(url=profile.avatar.url)
            await ctx.send(embed=embedVar)
            with open(f'profiles.json', 'w') as json_file:
                json.dump(profile_data, json_file)

    @commands.is_owner()
    @commands.command(name="debugwordle", help="waaaaorld")
    async def debugwordle(self, ctx, word):
        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and msg.content.lower()[0] in string.printable
        words = []
        with open('words.txt') as j:
            for line in j.readlines():
                words.append(line.strip())
        with open('words_also.txt') as j:
            for line in j.readlines():
                words.append(line.strip())
        word = word[0:5].lower()
        game = Spaces(word)
        embed = discord.Embed(title="Wordle")
        view = await ctx.send(embed=embed, view=game)
        guess_number = 0
        guesses = []
        while guess_number < 5:
            if(not game.value):
                embed=discord.Embed(title="You win!", color=0x00FF00)
                return await view.edit(embed=embed, view=game)
            guess = await self.bot.wait_for("message", check=check)
            if guess.content.lower() == 'exit' or guess.content.lower() == 'quit':
                game = Spaces(word, guesses, 'exit')
                await ctx.send("Quitting game...")
                return await view.edit(embed=embed, view=game)
            if len(guess.content) < 5:
                await guess.add_reaction('❌')
                embed = discord.Embed(title="Too Short! Guess again.")
                await view.edit(embed=embed, view=game)
                continue
            elif len(guess.content) > 5:
                await guess.add_reaction('❌')
                embed = discord.Embed(title="Too Long! Guess again.")
                await view.edit(embed=embed, view=game)
                continue
            elif guess.content not in words:
                await guess.add_reaction('❌')
                embed = discord.Embed(title="Word not in wordlist! Guess again.")
                await view.edit(embed=embed, view=game)
                continue
            else:
                guesses.append(guess.content.lower())
                embed = discord.Embed(title="Wordle")
                game = Spaces(word, guesses)
                await view.edit(embed=embed, view=game)
                guess_number += 1
        if(not game.value):
            embed=discord.Embed(title="You win!", color=0x00FF00)
            return await view.edit(embed=embed, view=game)
        else:
            embed = discord.Embed(title="You lose... Better luck next time!", description=f"The word was {word}", color=0xFF0000)
            await view.edit(embed=embed, view=game)

    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")


def setup(bot):
    bot.add_cog(Wordle(bot))