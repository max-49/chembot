import io
import os
import json
import string
import discord
import requests
import chat_exporter
from discord.ext import commands
from discord.ext.commands import has_permissions


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear', help="clears screen (admin only)")
    @has_permissions(administrator=True)
    async def clear(self, ctx):
        await ctx.send("_ _\n"*40)

    @commands.command(name='addquestion', help="owner only", hidden=True)
    async def addquestion(self, ctx, *params):
        if(ctx.author.id == 427832149173862400):
            def check(msg):
                return msg.author == ctx.author and msg.channel == msg.channel and \
                    msg.content.lower()[0] in string.printable

            def choices(msg):
                return msg.author == ctx.author and msg.channel == msg.channel and \
                    msg.content.lower() in ["a", "b", "c", "d"]

            def yesorno(msg):
                return msg.author == ctx.author and msg.channel == msg.channel and \
                    msg.content.lower() in ["yes", "no"]
            file = params[0]
            with open(f'questions/{file}.json') as f:
                question_data = json.load(f)
            try:
                past_number = question_data[-1]["number"]
                new_number = past_number + 1
            except IndexError:
                new_number = 0
            await ctx.send("Please enter the question")
            question = await self.bot.wait_for("message", check=check)
            await ctx.send("Please enter choice a")
            option_a = await self.bot.wait_for("message", check=check)
            await ctx.send("Please enter choice b")
            option_b = await self.bot.wait_for("message", check=check)
            await ctx.send("Please enter choice c")
            option_c = await self.bot.wait_for("message", check=check)
            await ctx.send("Please enter choice d")
            option_d = await self.bot.wait_for("message", check=check)
            await ctx.send("Please enter the answer")
            answer = await self.bot.wait_for("message", check=choices)
            await ctx.send("Is there an image with this question?")
            has_image = await self.bot.wait_for("message", check=yesorno)
            if(has_image.content == "yes"):
                await ctx.send("Please enter the imgur image link")
                image_link = await self.bot.wait_for("message", check=check)
                image = image_link.content
            else:
                image = 0
            await ctx.send("Does this question require the use of a calculator?")
            calculator = await self.bot.wait_for("message", check=yesorno)
            if(calculator.content == "yes"):
                need_calc = "True"
            else:
                need_calc = "False"
            await ctx.send("Does this question require the use of the reference table?")
            reference = await self.bot.wait_for("message", check=yesorno)
            if(reference.content == "yes"):
                need_reference = "True"
            else:
                need_reference = "False"

            question_data.append({"number": new_number, "question": question.content.replace('\n', ' '), "choices": [option_a.content.replace('\n', ' '), option_b.content.replace(
                '\n', ' '), option_c.content.replace('\n', ' '), option_d.content.replace('\n', ' ')], "answer": answer.content.replace('\n', ' '), "image": image, "Calc": need_calc, "Table": need_reference})
            with open(f'questions/{file}.json', 'w') as json_file:
                json.dump(question_data, json_file)
            await ctx.send("Question successfully added!")

    @commands.command(name='addworldquestion', help="owner only", hidden=True)
    async def addworldquestion(self, ctx):
        if(ctx.author.id == 427832149173862400 or ctx.author.id == 523309470105993226 or ctx.author.id == 293416817408475136):
            def check(msg):
                return msg.author == ctx.author and msg.channel == msg.channel and \
                    msg.content.lower()[0] in string.printable

            def choices(msg):
                return msg.author == ctx.author and msg.channel == msg.channel and \
                    msg.content.lower() in ["a", "b", "c", "d"]

            def yesorno(msg):
                return msg.author == ctx.author and msg.channel == msg.channel and \
                    msg.content.lower() in ["yes", "no"]
            with open('questions/apworld.json') as f:
                question_data = json.load(f)
            try:
                past_number = question_data[-1]["number"]
                new_number = past_number + 1
            except IndexError:
                new_number = 0
            await ctx.send("Please enter the question")
            question = await self.bot.wait_for("message", check=check)
            await ctx.send("Please enter choice a")
            option_a = await self.bot.wait_for("message", check=check)
            await ctx.send("Please enter choice b")
            option_b = await self.bot.wait_for("message", check=check)
            await ctx.send("Please enter choice c")
            option_c = await self.bot.wait_for("message", check=check)
            await ctx.send("Please enter choice d")
            option_d = await self.bot.wait_for("message", check=check)
            await ctx.send("Please enter the answer")
            answer = await self.bot.wait_for("message", check=choices)
            await ctx.send("Is there an image with this question?")
            has_image = await self.bot.wait_for("message", check=yesorno)
            if(has_image.content == "yes"):
                await ctx.send("Please enter the imgur image link")
                image_link = await self.bot.wait_for("message", check=check)
                image = image_link.content
            else:
                image = 0

            question_data.append({"number": new_number, "question": question.content.replace('\n', ' '), "choices": [option_a.content.replace('\n', ' '), option_b.content.replace(
                '\n', ' '), option_c.content.replace('\n', ' '), option_d.content.replace('\n', ' ')], "answer": answer.content.replace('\n', ' '), "image": image})
            with open('questions/apworld.json', 'w') as json_file:
                json.dump(question_data, json_file)
            await ctx.send("Question successfully added!")

    @commands.command(name='addstats', help="owner only", hidden=True)
    async def addstats(self, ctx):
        if(ctx.author.id == 427832149173862400):
            def check(msg):
                return msg.author == ctx.author and msg.channel == msg.channel and \
                    msg.content.lower()[0] in string.printable

            def choices(msg):
                return msg.author == ctx.author and msg.channel == msg.channel and \
                    msg.content.lower() in ["a", "b", "c", "d", "e"]
            with open('questions/apstats.json') as f:
                question_data = json.load(f)
            try:
                past_number = question_data[-1]["number"]
                new_number = past_number + 1
            except IndexError:
                new_number = 0
            await ctx.send("Please enter the imgur image link")
            image_link = await self.bot.wait_for("message", check=check)
            image = image_link.content
            await ctx.send("Please enter the answer")
            answer = await self.bot.wait_for("message", check=choices)
            question_data.append(
                {"number": new_number, "answer": answer.content, "image": image})
            with open('questions/apstats.json', 'w') as json_file:
                json.dump(question_data, json_file)
            await ctx.send("Question successfully added!")

    @commands.command(name='save', help="saves an archive of the chat!")
    async def save(self, ctx, *params):
        with open('allowed_ids.json') as j:
            allowed_ids = json.load(j)
        try:
            if(ctx.author.id == 427832149173862400 or ctx.author.guild_permissions.administrator):
                if(params[0] == "allowId"):
                    discord_json = requests.get(f"https://discord.com/api/v9/users/{params[1]}/profile", headers={"Authorization":f"Bot {os.getenv('CHEM_TOKEN')}"}).json()
                    print(discord_json)
                    if int(params[1]) not in allowed_ids:
                        allowed_ids.append(int(params[1])) 
                        await ctx.reply("Successfully added ID to allowed IDs!")
                    else:
                        await ctx.reply("This ID is already allowed to archive chats!")
                elif(params[0] == "denyId"):
                    if int(params[1]) in allowed_ids:
                        allowed_ids.remove(int(params[1]))
                        await ctx.reply("Successfully denied user from archiving chats!")
                    else:
                        await ctx.reply("This ID already isn't allowed to archive chats!")
        except IndexError:
            if(ctx.author.id == 427832149173862400 or ctx.author.guild_permissions.administrator or ctx.author.id in allowed_ids):
                await ctx.send("Saving...")
                transcript = await chat_exporter.export(ctx.channel, None, "EST")
                if transcript is None:
                    await ctx.reply("Save resulted in no transcript being created! Please try again.")
                    return
                transcript_file = discord.File(io.BytesIO(
                    transcript.encode()), filename=f"archive-{ctx.channel.name}.html")
                await ctx.reply(file=transcript_file)
        with open('allowed_ids.json', 'w') as j:
            json.dump(allowed_ids, j)

    @commands.command(name='adminstuff', hidden=True)
    async def adminstuff(self, ctx):
        embedVar = discord.Embed(color=0xadd8e6)
        embedVar.add_field(name="How to gain access to the server",
                           value="To gain access to the rest of the server, type **\"Tyler Bissoondial is a chad smurf\"** in this chat (case does not matter). Schlooth Bot will verify you soon after.", inline=False)
        await ctx.send(embed=embedVar)

    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")

def setup(bot):
    bot.add_cog(Admin(bot))
