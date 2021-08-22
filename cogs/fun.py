import os
import json
import string
import typing
import aiohttp
import discord
import asyncio
import requests
from random import randint
from datetime import datetime
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='chat', help="gives you the ability to chat with the bot", pass_context=True)
    async def chat(self, ctx, channel: typing.Optional[discord.TextChannel], *, message: str):
        await ctx.message.delete()
        if channel is None:
            await ctx.send(message)
        else:
            await channel.send(message)

    @commands.command(name='trivia', help="dispenses a user-submitted trivia question!", aliases=['triv'])
    async def trivia(self, ctx):
        with open('questions/trivia.json') as f:
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

        await ctx.reply(embed=embedVar)

        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and \
                msg.content.lower() in ["a", "b", "c", "d"]
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=120)
        except asyncio.TimeoutError:
            await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!")
        if msg.content.lower() == questions[question_number]['answer']:
            await msg.reply("Correct!")
        else:
            await msg.reply(f"Incorrect Answer. The correct answer was `{questions[question_number]['answer']}`")

    @commands.command(name='addtrivia', help="add a question to s!trivia!")
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
        with open('questions/trivia.json') as f:
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
        with open('questions/trivia.json', 'w') as json_file:
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
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                use_hook.url, adapter=AsyncWebhookAdapter(session))
            await webhook.send(message, username=ctx.author.display_name, avatar_url=ctx.author.avatar_url, allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=False))

    @commands.command(name="saym", help="impersonate someone!")
    async def saym(self, ctx, member: discord.Member, *, message: str):
        for webhook in await ctx.channel.webhooks():
            if str(webhook.user) == str(self.bot.user):
                use_hook = webhook
                break
        else:
            use_hook = await ctx.channel.create_webhook(name='chem')
        await ctx.message.delete()
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                use_hook.url, adapter=AsyncWebhookAdapter(session))
            await webhook.send(message, username=member.display_name, avatar_url=member.avatar_url, allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=False))

    @commands.command(name="stats", help="ictf stats on chembot lmao", pass_context=True)
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
            embedVar.add_field(name="Solved Challenges",
                               value=solved, inline=True)
            embedVar.add_field(name="Unsolved Challenges",
                               value=unsolved, inline=True)
            embedVar.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embedVar)
        except IndexError:
            await ctx.send("User is not on the leaderboard yet! Tell them to check out <https://imaginaryctf.org/>!")

    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")


def setup(bot):
    bot.add_cog(Fun(bot))
