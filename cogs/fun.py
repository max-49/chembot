import os
import json
import string
import typing
import aiohttp
import discord
import asyncio
import random
import requests
from random import randint
from datetime import datetime
from discord.ext import commands
from discord import Webhook, SyncWebhook


class Regents(discord.ui.View):
    def __init__(self, correct: str, category: str, choices: int, author: discord.Member):
        super().__init__()
        self.value = None
        self.correct = correct
        self.category = category
        self.choices = choices
        self.author = author
        if(self.choices != 5):
            self.remove_item(self.e)

    @discord.ui.button(label='A', style=discord.ButtonStyle.grey)
    async def a(self, button: discord.ui.Button, interaction: discord.Interaction):
        if(self.correct == 'a'):
            await interaction.response.send_message('Correct!', ephemeral=True)          
            button.style = discord.ButtonStyle.green
            self.value = True
        else:
            await interaction.response.send_message(f'Incorrect! The correct answer was {self.correct}. You should probably review the {self.category} unit.', ephemeral=True)
            button.style = discord.ButtonStyle.red
            self.value = False  
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        self.stop()

    @discord.ui.button(label='B', style=discord.ButtonStyle.grey)
    async def b(self, button: discord.ui.Button, interaction: discord.Interaction):
        if(self.correct == 'b'):
            await interaction.response.send_message('Correct!', ephemeral=True)         
            button.style = discord.ButtonStyle.green
            self.value = True
        else:
            await interaction.response.send_message(f'Incorrect! The correct answer was {self.correct}. You should probably review the {self.category} unit.', ephemeral=True)
            button.style = discord.ButtonStyle.red
            self.value = False
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        self.stop()

    @discord.ui.button(label='C', style=discord.ButtonStyle.grey)
    async def c(self, button: discord.ui.Button, interaction: discord.Interaction):
        if(self.correct == 'c'):
            await interaction.response.send_message('Correct!', ephemeral=True)     
            button.style = discord.ButtonStyle.green
            self.value = True       
        else:
            await interaction.response.send_message(f'Incorrect! The correct answer was {self.correct}. You should probably review the {self.category} unit.', ephemeral=True)
            button.style = discord.ButtonStyle.red
            self.value = False   
        for child in self.children:
            child.disabled = True        
        await interaction.message.edit(view=self)
        self.stop()
    
    @discord.ui.button(label='D', style=discord.ButtonStyle.grey)
    async def d(self, button: discord.ui.Button, interaction: discord.Interaction):
        if(self.correct == 'd'):
            await interaction.response.send_message('Correct!', ephemeral=True)
            button.style = discord.ButtonStyle.green
            self.value = True           
        else:
            await interaction.response.send_message(f'Incorrect! The correct answer was {self.correct}. You should probably review the {self.category} unit.', ephemeral=True)
            button.style = discord.ButtonStyle.red
            self.value = False
        for child in self.children:
            child.disabled = True  
        await interaction.message.edit(view=self)
        self.stop()

    @discord.ui.button(label='E', style=discord.ButtonStyle.grey)
    async def e(self, button: discord.ui.Button, interaction: discord.Interaction):
        if(self.correct == 'e'):
            await interaction.response.send_message('Correct!', ephemeral=True)
            button.style = discord.ButtonStyle.green
            self.value = True
        else:
            await interaction.response.send_message(f'Incorrect! The correct answer was {self.correct}. You should probably review the {self.category} unit.', ephemeral=True)   
            button.style = discord.ButtonStyle.red
            self.value = False  
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.author:
            return True
        else:
            await interaction.response.send_message('This button isn\'t for you!', ephemeral=True)
            return False


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='chat', help="gives you the ability to chat with the bot", pass_context=True)
    async def chat(self, ctx, channel: typing.Optional[discord.TextChannel], *, message: str):
        await ctx.message.delete()
        if channel is None:
            await ctx.send(message, allowed_mentions=discord.AllowedMentions(everyone=False))
        else:
            await channel.send(message, allowed_mentions=discord.AllowedMentions(everyone=False))

    @commands.command(name='trivia', help="dispenses a user-submitted trivia question!", aliases=['triv'])
    async def trivia(self, ctx):
        with open('trivia/trivia.json') as f:
            questions = json.load(f)
        question_number = int(randint(0, len(questions)-1))

        embedVar = discord.Embed(
            title="Question #" + str(question_number + 1), timestamp=datetime.utcnow(), color=0x00C3FF)

        if(questions[question_number]['image'] != 0):
            embedVar.set_image(url=questions[question_number]['image'])

        embedVar.add_field(name=questions[question_number]['question'], value="a) " + str(questions[question_number]['choices'][0]) + "\nb) " + str(
            questions[question_number]['choices'][1]) + "\nc) " + str(questions[question_number]['choices'][2]) + "\nd) " + str(questions[question_number]['choices'][3]), inline=False)

        embedVar.add_field(
            name="Added by:", value=questions[question_number]['creator'])

        regents = Regents(questions[question_number]['answer'], "Trivia", 4, ctx.author)

        await ctx.reply(embed=embedVar, view=regents)

        await regents.wait()
        if regents.value is None:
            await ctx.reply(f"Sorry {ctx.author.display_name}, you didn't reply in time!")

    @commands.command(name='addtrivia', aliases=['addtriv'], help="add a question to s!trivia!")
    async def addtrivia(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and \
                msg.content.lower()[0] in string.printable

        def choices(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and \
                msg.content.lower() in ["a", "b", "c", "d"]

        def yesorno(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and \
                msg.content.lower() in ["yes", "no"]
        await ctx.send(f"{ctx.author.mention}, please enter the question (no questions with newlines)")
        question = await self.bot.wait_for("message", check=check)
        await ctx.send(f"{ctx.author.mention}, please enter choice a")
        option_a = await self.bot.wait_for("message", check=check)
        await ctx.send(f"{ctx.author.mention}, please enter choice b")
        option_b = await self.bot.wait_for("message", check=check)
        await ctx.send(f"{ctx.author.mention}, please enter choice c")
        option_c = await self.bot.wait_for("message", check=check)
        await ctx.send(f"{ctx.author.mention}, please enter choice d")
        option_d = await self.bot.wait_for("message", check=check)
        await ctx.send(f"{ctx.author.mention}, please enter the answer")
        answer = await self.bot.wait_for("message", check=choices)
        await ctx.send(f"{ctx.author.mention}, is there an image with this question?")
        has_image = await self.bot.wait_for("message", check=yesorno)
        with open('trivia/trivia.json') as f:
            question_data = json.load(f)
        if(has_image.content == "yes"):
            await ctx.send("Please enter the imgur image link")
            image_link = await self.bot.wait_for("message", check=check)
            image = image_link.content
        else:
            image = 0
        try:
            past_number = question_data[-1]["number"]
            new_number = past_number + 1
        except IndexError:
            new_number = 0
        question_data.append({"number": new_number, "question": question.content.replace('\n', ' '), "choices": [option_a.content.replace('\n', ' '), option_b.content.replace(
            '\n', ' '), option_c.content.replace('\n', ' '), option_d.content.replace('\n', ' ')], "answer": (answer.content.replace('\n', ' ')).lower(), "image": image, "creator": ctx.author.name})
        with open('trivia/trivia.json', 'w') as json_file:
            json.dump(question_data, json_file)
        await ctx.send(f"{ctx.author.mention}, your question was successfully added!")

    @commands.command(name="say", help="say something as a webhook!")
    async def say(self, ctx, *, message: str):
        message = message.replace('\'', '\'').replace(
            '\"', '\"').replace('\\', '\\')
        for webhook in await ctx.channel.webhooks():
            if str(webhook.user) == str(self.bot.user):
                use_hook = webhook
                break
        else:
            use_hook = await ctx.channel.create_webhook(name='chem')
        await ctx.message.delete()
        webhook = SyncWebhook.from_url(use_hook.url)
        webhook.send(message, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url, allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=False))

    @commands.command(name="saym", help="impersonate someone!")
    async def saym(self, ctx, member: discord.Member, *, message: str):
        for webhook in await ctx.channel.webhooks():
            if str(webhook.user) == str(self.bot.user):
                use_hook = webhook
                break
        else:
            use_hook = await ctx.channel.create_webhook(name='chem')
        await ctx.message.delete()
        webhook = SyncWebhook.from_url(use_hook.url)
        webhook.send(message, username=member.display_name, avatar_url=member.avatar.url, allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=False))

    @commands.command(name="ictfstats", help="ictf stats on chembot lmao", pass_context=True)
    async def stats(self, ctx, member: discord.Member = None):
        try:
            if member is None:
                member = ctx.author
            all_challs = (requests.get(
                'https://imaginaryctf.org/api/challenges/released')).json()
            my_challs = (requests.get(
                f'https://imaginaryctf.org/api/solves/bydiscordid/{member.id}')).json()
            if(my_challs[0]["team"] != None):
                my_challs = (requests.get(
                    f'https://imaginaryctf.org/api/solves/byteamid/{my_challs[0]["team"]["id"]}')).json()
                score = my_challs[0]["team"]["score"]
                name = str(my_challs[0]["team"]["name"]) + " (team)"
            else:
                score = my_challs[0]["user"]["score"]
                name = member.name
            all_solves = []
            all_list = []
            all_list_alt = []
            for i in range(len(my_challs)):
                all_solves.append(my_challs[i]["challenge"]["title"])
            for i in range(len(all_challs)):
                all_list.append(all_challs[i]["title"])
            for thing in all_list:
                all_list_alt.append(thing)
            for thing in all_list_alt:
                if(thing in all_solves):
                    all_list.remove(thing)
            all_solves.reverse()
            all_list.reverse()
            solved = '\n'.join(all_solves)
            unsolved = '\n'.join(all_list)
            embedVar = discord.Embed(title=f"Stats for {name}", color=0x3498DB)
            embedVar.add_field(name="Score", value=score, inline=False)
            if(len(solved) > 3):
                embedVar.add_field(name="Solved Challenges", value=solved, inline=True)
            if(len(unsolved) > 3):
                embedVar.add_field(name="Unsolved Challenges", value=unsolved, inline=True)
            embedVar.set_thumbnail(url=member.avatar.url)
            await ctx.send(embed=embedVar)
        except IndexError:
            await ctx.send("User is not on the leaderboard yet! Tell them to check out <https://imaginaryctf.org/>!")

    @commands.command(name='8ball', help='ask your question! 8ball <question>')
    async def ball(self, ctx, question=None):
        if(not question):
            await ctx.reply('You must ask a question!')
            return
        with open('ball.json') as j:
            responses = json.load(j)
        question = question.replace('i', str(ctx.author.name)).replace('I', str(ctx.author.name))
        title = question if len(question) < 75 else '8ball'
        embed = discord.Embed(title=title)
        embed.add_field(name=f'{str(self.bot.user.name).split()[0]} says', value='\u200b')
        mess = await ctx.send(embed=embed)
        num = random.randint(1,8)
        for i in range(num):
            await asyncio.sleep(1)
            embed = discord.Embed(title=title)
            embed.add_field(name=f'{str(self.bot.user.name).split()[0]} says' + '.'*(i+1), value='\u200b')
            new_mess = await mess.edit(embed=embed)
        await asyncio.sleep(1)
        embed = discord.Embed(title=title, color=0xFFFF00)
        embed.add_field(name=f'{str(self.bot.user.name).split()[0]} says' + '.'*(num+1), value=random.choice(responses))
        await new_mess.edit(embed=embed)

    @commands.command(name='add8ball', help='add a response to 8ball!')
    async def addball(self, ctx, *, res=None):
        with open('ball.json') as j:
            responses = json.load(j)
        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and msg.content.lower()[0] in string.printable
        if not res:
            await ctx.send(f"{ctx.author.mention}, please enter the 8ball reason you would like to be added.")
            response = await self.bot.wait_for("message", check=check)
            responses.append(response.content)
        else:
            responses.append(res)
        with open('ball.json', 'w') as j:
            json.dump(responses, j)
        await ctx.send(f"{ctx.author.mention}, your 8ball response has successfully been added!")

    @commands.command(name='choose', help='chooses a random item! syntax: choose <question> [choices]')
    async def choose(self, ctx, question, *choices):
        question = question.replace('i', str(ctx.author.name)).replace('I', str(ctx.author.name))
        title = question if len(question) < 75 else '8ball'
        if(len(question.split()) < 2):
            message = f"{str(self.bot.user.name).split()[0]} chooses "
        else:
            message = question
        if(len(choices) > 10):
            await ctx.reply("Too many choices!")
            return
        choice = random.choice(list(choices))
        embed = discord.Embed(title=title)
        embed.add_field(name=f"**{message}**", value='\u200b')
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(random.randint(1,5))
        embed = discord.Embed(title=title, color=0xFFFF00)
        embed.add_field(name=f"**{message}**", value=f"{choice}")
        await msg.edit(embed=embed)


    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")


def setup(bot):
    bot.add_cog(Fun(bot))
