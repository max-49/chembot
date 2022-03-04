import os
import json
import random
import string
import discord
from datetime import datetime
from discord.ext import commands
from discord.ui.button import Button

'''
This is the Spaces class, the callback class that is required for any discord.py view, in this case, for buttons. 
This class is called whenever a new word is inputted or the game is quit.
When a new word is inputted, it compares the word to the real word and decides whether the button should be gray, green, or purple, following standard Wordle rules.
When an exit (exitt in __init__) parameter is sent (sent when a user manually quits or runs out of guesses), all buttons are deactivated and the game ends.
'''
class Spaces(discord.ui.View):
    def __init__(self, bot, word_num, word: str, guesses=None, exitt=None):
        super().__init__()
        self.wordle = [f"{(''.join(bot.user.name.split()))[:4]}ordle {word_num} ", ""]
        for _ in range(25):
            self.add_item(Button(label='\u200b', style=discord.ButtonStyle.grey))
        word = word.upper()
        self.value = True
        self.guesses = guesses if guesses is not None else []
        for j, guess in enumerate(self.guesses):
            self.change_colors(j, guess, word, exitt)

    def change_colors(self, j, guess, word, exitt):
        colors = {discord.ButtonStyle.green: "🟩", discord.ButtonStyle.blurple: "🟪", discord.ButtonStyle.grey: "⬛"}
        for i, (x,y) in enumerate(zip(guess, word)):
            self.children[i + 5 * j].label = x
            # button should be green if the guess and word have the same letter in the same spot
            if x == y:
                self.children[i + 5 * j].style = discord.ButtonStyle.green
            # button should be purple if the letter in the guess is in the word, but in the incorrect spot. Additionally, if there are two of a purple letter in the guess but only one of those in the word, only one of those should be purple, the other should be black.
            elif y in guess:
                guess_indices = [p for p, c in enumerate(guess) if c == y and self.children[p + 5 * j].style != discord.ButtonStyle.green]
                word_indices = [p for p, c in enumerate(word) if c == y and p not in guess_indices and self.children[p + 5 * j].style != discord.ButtonStyle.green]
                for i in range(min(len(word_indices), len(guess_indices))):
                    self.children[guess_indices[i] + 5 * j].style = discord.ButtonStyle.blurple
        # if an exit is sent, disable all the buttons
        squares = ""
        if guess == word or (exitt is not None and j == len(self.guesses)-1):
            self.wordle[0] += "X/5" if exitt is not None else f"{self.guesses.index(guess)+1}/5"
            for i, child in enumerate(self.children):
                if child.label != '\u200b':
                    squares += colors[child.style]
                child.disabled = True
            self.wordle += [squares[i:i+5] for i in range(0, len(squares), 5)]
            self.value = False

'''
This is the Wordle class, a discord.py cog that hold all commands in the Wordle help category
'''
class Wordle(commands.Cog):
    '''
    The wordlist is imported from the word files in the __init__ function
    '''
    def __init__(self, bot):
        self.bot = bot
        self.words = []
        with open('words.txt') as j:
            for line in j.readlines():
                self.words.append(line.strip())
        self.also_words = []
        with open('words_also.txt') as j:
            for line in j.readlines():
                self.also_words.append(line.strip())

    '''
    When a user runs the wordle command, a word is selected from the "words" list and a game is initialized.
    From there, the user has 5 tries to guess the word. When a word is inputted, it is checked to make sure it is 5 letters long 
    and is in the wordlist and if it satisfies those conditions, it is deleted and sent to the Spaces() class for determining colors.
    If the user guesses the word, the value of the Spaces "view" will be set to False, and the command will prompt a win scene.
    If the user quits early, no scene changes are done and the buttons just deactivate.
    If the user fails to guess the word in 5 tries, the buttons deactivate and a lose scene is prompted. 
    After a win or lose, the user's profile is updated
    '''
    @commands.command(name="wordle", help="world")
    async def wordle(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower()[0] in string.printable
        
        # select a word and define wordlist
        word = random.choice(self.words)
        wordlist = self.words + self.also_words

        # initialize game
        game = Spaces(self.bot, wordlist.index(word), word)
        embed = discord.Embed(title="Wordle")
        view = await ctx.send(embed=embed, view=game)

        guess_number = 0
        guesses = []
        while guess_number < 5 and game.value:
            # get user input for the guess
            guess = await self.bot.wait_for("message", check=check)
            # send exit to the Spaces() class if user quits early
            if guess.content.lower() == 'exit' or guess.content.lower() == 'quit':
                game = Spaces(self.bot, wordlist.index(word), word, guesses, 'exit')
                await ctx.send("Quitting game...")
                return await view.edit(embed=embed, view=game)
            # checks if word is valid
            if len(guess.content) < 5 or len(guess.content) > 5 or guess.content.lower() not in wordlist:
                await guess.add_reaction('❌')
                embed = discord.Embed(title="Invalid word! Guess again.")
                await view.edit(embed=embed, view=game)
            else:
                guesses.append(guess.content.upper())
                embed = discord.Embed(title="Wordle")
                game = Spaces(self.bot, wordlist.index(word), word, guesses)
                await view.edit(embed=embed, view=game)
                await guess.delete()
                guess_number += 1
    
        with open(f'profiles.json') as f:
            profile_data = json.load(f)
        
        user_id = 0
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == ctx.author.id):
                profile_data[i]['WordleTotal'] = profile_data[i]['WordleTotal'] + 1 
                user_id = i

        if(not game.value):
            embed=discord.Embed(title="You win!", color=0x00FF00)
            profile_data[user_id]['WordleWins'] = profile_data[user_id]['WordleWins'] + 1
            await view.edit(embed=embed, view=game)
            await ctx.send('\n'.join(game.wordle))
        else:
            embed = discord.Embed(title="You lose... Better luck next time!", description=f"The word was {word}", color=0xFF0000)
            game = Spaces(self.bot, wordlist.index(word), word, guesses, "exit")
            await view.edit(embed=embed, view=game)
            await ctx.send('\n'.join(game.wordle))
        
        with open('profiles.json', 'w') as j:
            json.dump(profile_data, j)
        
    '''
    This command is the same as the profile command but just returns the user's wordle stats.
    It will initialize a user profile if the user does not have one.
    '''
    @commands.command(name="wordlestats", help="wordle stats")
    async def wordlestats(self, ctx, profile: discord.Member=None):
        with open(f'profiles.json') as f:
            profile_data = json.load(f)
        
        uid = ctx.author.id if profile is None else profile.id
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == uid):
                embed = discord.Embed(title=f"{profile_data[i]['Name']}'s profile",  timestamp=datetime.utcnow(), color=0x00ff00)
                try:
                    percent_correct = (profile_data[i]['WordleWins']/profile_data[i]['WordleTotal']) * 100
                except ZeroDivisionError:
                    percent_correct = 0
                embed.add_field(name="Wordle Stats", value=f"{str(profile_data[i]['WordleWins'])}/{str(profile_data[i]['WordleTotal'])} ({str(round(percent_correct, 2))}%)", inline=False)
                embed.set_thumbnail(url=profile_data[i]['Avatar URL'])
                await ctx.send(embed=embed)
                return
        if profile is None:
            profile = ctx.author
        profile_data.append({"Name": profile.name, "Tag": str(profile), "Nick": profile.display_name, "ID": profile.id, "Avatar URL": str(profile.avatar.url), "Correct": 0, "Total": 0, "Calc": "True", "Table": "True", "WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1, "Times": 0, "Win": 0, "Lose": 0, "Profit": 0, "WordleWins": 0, "WordleTotal": 0, "didDaily": False})
        embed = discord.Embed(title=f"{profile.name}'s profile",  timestamp=datetime.utcnow(), color=0x00ff00)
        percent_correct = 0
        embed.add_field(name="Profile initialized!", value="Run the command again to see your profile!", inline=False)
        embed.set_thumbnail(url=profile.avatar.url)
        await ctx.send(embed=embed)
        with open(f'profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    '''
    This a command for the owner of the bot to debug the wordle command. 
    The differences between this command and the normal wordle command are that this command has you choose your own word,
    does not check the wordlist for valid words, and has no effect on the user's stats.
    '''
    @commands.is_owner()
    @commands.command(name="debugwordle", help="waaaaorld")
    async def debugwordle(self, ctx, word):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower()[0] in string.printable
        game = Spaces(self.bot, 0, word)
        embed = discord.Embed(title="Wordle")
        view = await ctx.send(embed=embed, view=game)

        guess_number = 0
        guesses = []
        while guess_number < 5 and game.value:
            guess = await self.bot.wait_for("message", check=check)
            if guess.content.lower() == 'exit' or guess.content.lower() == 'quit':
                game = Spaces(self.bot, 0, word, guesses, 'exit')
                await ctx.send("Quitting game...")
                return await view.edit(embed=embed, view=game)

            if len(guess.content) < 5 or len(guess.content) > 5:
                await guess.add_reaction('❌')
                embed = discord.Embed(title="Invalid word! Guess again.")
                await view.edit(embed=embed, view=game)
            else:
                guesses.append(guess.content.upper())
                embed = discord.Embed(title="Wordle")
                game = Spaces(self.bot, 0, word, guesses)
                await view.edit(embed=embed, view=game)
                await guess.delete()
                guess_number += 1
    
        if(not game.value):
            embed=discord.Embed(title="You win!", color=0x00FF00)
            await view.edit(embed=embed, view=game)
            await ctx.send('\n'.join(game.wordle))
        else:
            embed = discord.Embed(title="You lose... Better luck next time!", description=f"The word was {word}", color=0xFF0000)
            game = Spaces(self.bot, 0, word, guesses, "exit")
            await view.edit(embed=embed, view=game)
            await ctx.send('\n'.join(game.wordle))

    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")


def setup(bot):
    bot.add_cog(Wordle(bot))