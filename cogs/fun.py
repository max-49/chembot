import os
import json
import string
import typing
import aiohttp
import discord
import asyncio
import random
import requests
import youtube_dl
from random import randint
from datetime import datetime
from discord.ext import commands
from discord import SyncWebhook


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

# youtube_dl.utils.bug_reports_message = lambda: ''

# ytdl_format_options = {
#     'format': 'bestaudio/best',
#     'restrictfilenames': True,
#     'noplaylist': True,
#     'nocheckcertificate': True,
#     'ignoreerrors': False,
#     'logtostderr': False,
#     'quiet': True,
#     'no_warnings': True,
#     'default_search': 'auto',
#     'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
# }

# ffmpeg_options = {
#     'options': '-vn'
# }

# ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)
#         self.data = data
#         self.title = data.get('title')
#         self.url = ""

#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
#         if 'entries' in data:
#             # take first item from a playlist
#             data = data['entries'][0]
#         filename = data['title'] if stream else ytdl.prepare_filename(data)
#         return filename

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="joinvc", help="join a voice channel")
    async def joinvc(self, ctx, *, channel: discord.VoiceChannel = None):
        if channel is None and ctx.author.voice.channel is None:
            return await ctx.send("You are not in a voice channel.")
        await channel.connect()
    
    @commands.command(name="leavevc", help="leave a voice channel")
    async def leavevc(self, ctx):
        await ctx.voice_client.disconnect()

    # @commands.command(name='play', help='To play song')
    # async def play(self, ctx, url: str):
    #     if ctx.voice_client is None:
    #         await ctx.invoke(self.joinvc)
    #     async with ctx.typing():
    #         filename = await YTDLSource.from_url(url, loop=self.bot.loop)
    #         ctx.voice_client.play(discord.FFmpegPCMAudio(executable="/bin/ffmpeg", source=filename))
    #     await ctx.send('**Now playing song**')

    # @commands.command(name='pause', help='This command pauses the song')
    # async def pause(self, ctx):
    #     if ctx.voice_client.is_playing():
    #         await ctx.voice_client.pause()
    #         await ctx.send("paused")
    #     else:
    #         await ctx.send("no.")
        
    # @commands.command(name='resume', help='Resumes the song')
    # async def resume(self, ctx):
    #     if ctx.voice_client.is_paused():
    #         await ctx.voice_client.resume()
    #         await ctx.send('resumed')
    #     else:
    #         await ctx.send("no.")

    # @commands.command(name='stop', help='Stops the song')
    # async def stop(self, ctx):
    #     if ctx.voice_client.is_playing():
    #         await ctx.voice_client.stop()
    #         await ctx.send('stopped')
    #     else:
    #         await ctx.send("no.")

    @commands.command(name='chat', help="gives you the ability to chat with the bot", pass_context=True)
    async def chat(self, ctx, channel: typing.Optional[discord.TextChannel], *, message: str):
        await ctx.message.delete()
        if channel is None:
            await ctx.send(message, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True, replied_user=False))
        else:
            await channel.send(message, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True, replied_user=False))

    @commands.command(name='trivia', help="dispenses a user-submitted trivia question!", aliases=['triv', 'tri', 't'])
    async def trivia(self, ctx, num: int=None):
        with open('trivia/trivia.json') as f:
            questions = json.load(f)
        if not num:
            question_number = int(randint(0, len(questions)-1))
        else:
            question_number = num - 1

        embed = discord.Embed(
            title="Question #" + str(question_number + 1), timestamp=datetime.utcnow(), color=0x00C3FF)

        if(questions[question_number]['image'] != 0):
            embed.set_image(url=questions[question_number]['image'])

        embed.add_field(name=questions[question_number]['question'], value="a) " + str(questions[question_number]['choices'][0]) + "\nb) " + str(
            questions[question_number]['choices'][1]) + "\nc) " + str(questions[question_number]['choices'][2]) + "\nd) " + str(questions[question_number]['choices'][3]), inline=False)

        embed.add_field(
            name="Added by:", value=questions[question_number]['creator'])

        regents = Regents(questions[question_number]['answer'], "Trivia", 4, ctx.author)

        await ctx.reply(embed=embed, view=regents)

        await regents.wait()
        if regents.value is None:
            await ctx.reply(f"Sorry {ctx.author.display_name}, you didn't reply in time!")

    @commands.command(name='addtrivia', aliases=['addtriv', 'at'], help="add a question to s!trivia!")
    async def addtrivia(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and \
                msg.content.lower()[0] in string.printable

        def choices(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and \
                msg.content.lower() in ["a", "b", "c", "d"]

        def yesorno(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and \
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
        message = message.replace('\'', '\'').replace('\"', '\"').replace('\\', '\\')
        if len(message) > 150:
            message = message[:150]
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
        if len(message) > 150:
            message = message[:150]
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
                name = str(my_challs[0]["team"]["name"]) + " (team)"
            else:
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
            embed = discord.Embed(title=f"Stats for {name}", color=0x3498DB)
            embed.add_field(name="Score", value="really good :yep:", inline=False)
            if(len(solved) > 3):
                embed.add_field(name="Solved Challenges", value=solved, inline=True)
            if(len(unsolved) > 3):
                embed.add_field(name="Unsolved Challenges", value=unsolved, inline=True)
            embed.set_thumbnail(url=member.avatar.url)
            await ctx.send(embed=embed)
        except IndexError:
            await ctx.send("User is not on the leaderboard yet! Tell them to check out <https://imaginaryctf.org/>!")

    @commands.command(name='8ball', aliases=['ball', '8'], help='ask your question! 8ball <question>')
    async def ball(self, ctx, *, question=None):
        if(not question):
            await ctx.reply('You must ask a question!')
            return
        with open('ball.json') as j:
            responses = json.load(j)
        question = question.capitalize().replace(' i ', f" {str(ctx.author.name)} ").replace(' I ', f" {str(ctx.author.name)} ")
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

    @commands.command(name='add8ball', help='add a response to 8ball!', aliases=['addball', 'add8'])
    async def addball(self, ctx, *, res=None):
        with open('ball.json') as j:
            responses = json.load(j)
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower()[0] in string.printable
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
        question = question.capitalize().replace(' i ', f" {str(ctx.author.name)} ").replace(' I ', f" {str(ctx.author.name)} ")
        title = question if len(question) < 75 else 'Choices'
        message = f"{str(self.bot.user.name).split()[0]} chooses "
        if(len(choices) > 30):
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
