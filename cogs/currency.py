import os
import json
import math
import string
import asyncio
import discord
from config import get_bot
from random import randint
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import has_permissions


class Currency(commands.Cog):
    def __init__(self, bot):
        self.info = get_bot(os.getcwd().split('/')[-2])
        self.bot = bot

    @commands.command(name="balance", aliases=['bal', 'money'], help="displays your balance!")
    async def bal(self, ctx, profile="none"):
        with open('profiles.json') as f:
            profile_data = json.load(f)
        if(profile != "none"):
            uid = profile
            try:
                uid = int(uid)
            except ValueError:
                uid = profile
        else:
            uid = ctx.author.id
        found = 0
        for i in range(len(profile_data)):
            user_mention = f"<@!{profile_data[i]['ID']}>"
            if(profile_data[i]['ID'] == uid or profile_data[i]['Name'] == uid or profile_data[i]['Nick'] == uid or profile_data[i]['Tag'] == uid or user_mention == uid):
                found = 1
                embedVar = discord.Embed(
                    title=f"{profile_data[i]['Name']}'s balance", timestamp=datetime.utcnow(), color=0x00C3FF)
                embedVar.add_field(
                    name="Balance", value=f"{profile_data[i]['Balance']} {self.info[2]}", inline=False)
                await ctx.reply(embed=embedVar)
        if(found == 0):
            await ctx.send("No profile found!")
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    @commands.command(name="resetcooldown", help="resets your work cooldown with permission from the owner.")
    async def resetcool(self, ctx):
        if(ctx.author.id == 427832149173862400):
            self.work.reset_cooldown(ctx)
            await ctx.send("Work cooldown reset!")
        else:
            await ctx.send("You will be granted a cooldown reset if Max replies with 'yes' in the next 10 seconds")

            def check(msg):
                return str(msg.author) == "Max49#9833" and msg.channel == msg.channel
            while True:
                try:
                    msg = await self.bot.wait_for("message", check=check, timeout=10)
                except asyncio.TimeoutError:
                    await ctx.send("Max did not reply in time")
                    await ctx.send("No reset for you.")
                    break
                if(msg.content.lower() == "yes"):
                    self.work.reset_cooldown(ctx)
                    await ctx.send("Work cooldown reset!")
                    break
                else:
                    await ctx.send("No reset for you.")
                    break

    @commands.command(name="work", help="work")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def work(self, ctx, *params):
        with open('profiles.json') as f:
            profiles = json.load(f)
        try:
            with open('work/jobs.json') as f:
                jobs = json.load(f)
            job_list = []
            for thing in jobs:
                for key, value in thing.items():
                    if(key == "name"):
                        job_list.append(value)
            if(params[0] == "list"):
                embedVar = discord.Embed(
                    title="Currently Available Jobs", timestamp=datetime.utcnow(), color=0x00C3FF)
                msg = ""
                for i in range(len(jobs)):
                    msg += f"{jobs[i]['name']}: {jobs[i]['base_salary']} {self.info[2]}\n"
                embedVar.add_field(name="Jobs", value=msg, inline=False)
                embedVar.add_field(
                    name="\u200b", value=f"Do `{self.info[3]}work <job>` to select a job!")
                await ctx.reply(embed=embedVar)
                self.work.reset_cooldown(ctx)
                return 0
            if(str(params[0]).lower() in job_list):
                for i in range(len(profiles)):
                    for j in range(len(job_list)):
                        if(jobs[j]['name'] == str(params[0]).lower()):
                            job_index = j
                    if(profiles[i]['ID'] == ctx.author.id):
                        if(profiles[i]['Job'] == ""):
                            profiles[i]['Job'] = str(params[0]).lower()
                            profiles[i]['Salary'] = jobs[job_index]['base_salary']
                            await ctx.reply(f"You are now working as a `{str(params[0]).lower()}`! Do `{self.info[3]}work` to start working and making {self.info[2]}!")
                            with open('profiles.json', 'w') as json_file:
                                json.dump(profiles, json_file)
                            self.work.reset_cooldown(ctx)
                            return 0
                        else:
                            await ctx.reply(f"You're already working as a {profiles[i]['Job']}! Please do `{self.info[3]}work resign` to choose a new job.")
                            self.work.reset_cooldown(ctx)
                            return 0
                else:
                    await ctx.send(f"You don't have a profile yet! Do {self.info[3]}profile to create a profile and start working!")
                    self.work.reset_cooldown(ctx)
                    return 0
            if(str(params[0]).lower() == "resign"):
                for i in range(len(profiles)):
                    if(profiles[i]['ID'] == ctx.author.id):
                        if(profiles[i]['Job'] != ""):
                            old_job = profiles[i]['Job']
                            profiles[i]['Job'] = ""
                            profiles[i]['Salary'] = 0
                            profiles[i]['xp'] = 0
                            profiles[i]['level'] = 1
                            await ctx.reply(f"You have resigned from your job as a `{old_job}`! Select a new job from `{self.info[3]}work list` to start working again!")
                            with open('profiles.json', 'w') as json_file:
                                json.dump(profiles, json_file)
                            self.work.reset_cooldown(ctx)
                            return 0
                        else:
                            await ctx.reply(f"You're already don't have a job! Select a job fron `{self.info[3]}work list`!")
                            self.work.reset_cooldown(ctx)
                        return 0
        except IndexError:
            l = 0
        for i in range(len(profiles)):
            if(profiles[i]['ID'] == ctx.author.id):
                if(profiles[i]['Job'] == ""):
                    await ctx.reply(f"You don't have a job yet! Please choose one at `{self.info[3]}work list`")
                    self.work.reset_cooldown(ctx)
                    return 0
                else:
                    # check for promotion
                    if(profiles[i]['xp'] > (100 + (profiles[i]['level'] * 1.5))):
                        embedVar = discord.Embed(
                            title="Promotion!", timestamp=datetime.utcnow(), color=0xFFC0CB)
                        embedVar.add_field(name=f"Congratulations {ctx.author.name}! You've been working hard recently and have worked your way up to a promotion!",
                                           value=f"Level: **{profiles[i]['level']}** --> **{profiles[i]['level'] + 1}**\nSalary: **{profiles[i]['Salary']} {self.info[2]}** --> **{math.floor(profiles[i]['Salary'] * 1.5)} {self.info[2]}**")
                        profiles[i]['level'] += 1
                        profiles[i]['xp'] = 0
                        profiles[i]['Salary'] = math.floor(
                            profiles[i]['Salary'] * 1.5)
                        await ctx.reply(embed=embedVar)
                        self.work.reset_cooldown(ctx)
                        with open('profiles.json', 'w') as json_file:
                            json.dump(profiles, json_file)
                        return 0
                    with open(f"work/{profiles[i]['Job']}.json") as f:
                        work_scens = json.load(f)
                    scen = randint(0, len(work_scens)-1)
                    embedVar = discord.Embed(
                        title=f"Work as a {profiles[i]['Job']}", color=0x00C3FF)
                    embedVar.add_field(
                        name=f"**{work_scens[scen]['type']}** - {work_scens[scen]['desc']}", value=f"`{work_scens[scen]['prompt']}`")
                    await ctx.reply(embed=embedVar)
                    attempts = 2

                    def check(msg):
                        return msg.author == ctx.author and msg.channel == msg.channel
                    while True:
                        try:
                            msg = await self.bot.wait_for("message", check=check, timeout=120)
                        except asyncio.TimeoutError:
                            await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!")
                            break
                        if msg.content.lower() == str(work_scens[scen]['answer']).lower():
                            correctEmbed = discord.Embed(color=0x00FF00)
                            correctEmbed.add_field(
                                name="Nice job!", value=f"You've earned {profiles[i]['Salary']} {self.info[2]} for working!")
                            profiles[i]['Balance'] += profiles[i]['Salary']
                            xp_given = randint(0, 20)
                            profiles[i]['xp'] += xp_given
                            await msg.reply(embed=correctEmbed)
                            break
                        else:
                            if(attempts != 0):
                                await msg.reply(f"Incorrect answer. You have {attempts} attempts left")
                                attempts -= 1
                                continue
                            else:
                                profiles[i]['Balance'] += math.floor(
                                    int(profiles[i]['Salary'])/3)
                                await msg.reply(f"Incorrect Answer. The correct answer was `{work_scens[scen]['answer']}`. You've earned {math.floor(int(profiles[i]['Salary'])/3)} {self.info[2]} for working.")
                                break
        with open('profiles.json', 'w') as json_file:
            json.dump(profiles, json_file)

    @work.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cd = round(error.retry_after)
            minutes = str(cd // 60)
            seconds = str(cd % 60)
            em = discord.Embed(title=f"You can only work once per 5 minutes!",
                               description=f"Try again in {minutes} minutes and {seconds} seconds.", color=0xFF0000)
            await ctx.send(embed=em)

    @commands.command(name="worklist", help="Displays the list of jobs.")
    async def worklist(self, ctx):
        with open('work/jobs.json') as f:
            jobs = json.load(f)
        job_list = []
        for thing in jobs:
            for key, value in thing.items():
                if(key == "name"):
                    job_list.append(value)
        embedVar = discord.Embed(
            title="Currently Available Jobs", timestamp=datetime.utcnow(), color=0x00C3FF)
        msg = ""
        for i in range(len(jobs)):
            msg += f"{jobs[i]['name']}: {jobs[i]['base_salary']} {self.info[2]}\n"
        embedVar.add_field(name="Jobs", value=msg, inline=False)
        embedVar.add_field(
            name="\u200b", value=f"Do `{self.info[3]}work <job>` to select a job!")
        await ctx.reply(embed=embedVar)

    @commands.command(name="workresign", help="resign from work")
    async def resign(self, ctx):
        with open('profiles.json') as f:
            profiles = json.load(f)
        with open('work/jobs.json') as f:
            jobs = json.load(f)
        job_list = []
        for thing in jobs:
            for key, value in thing.items():
                if(key == "name"):
                    job_list.append(value)
        for i in range(len(profiles)):
            if(profiles[i]['ID'] == ctx.author.id):
                if(profiles[i]['Job'] != ""):
                    old_job = profiles[i]['Job']
                    profiles[i]['Job'] = ""
                    profiles[i]['Salary'] = 0
                    profiles[i]['xp'] = 0
                    profiles[i]['level'] = 1
                    await ctx.reply(f"You have resigned from your job as a `{old_job}`! Select a new job from `{self.info[3]}work list` to start working again!")
                    with open('profiles.json', 'w') as json_file:
                        json.dump(profiles, json_file)
                    self.work.reset_cooldown(ctx)
                else:
                    await ctx.reply(f"You're already don't have a job! Select a job fron `{self.info[3]}work list`!")
                    self.work.reset_cooldown(ctx)

    @commands.command(name="addwork", help="add a job work!")
    async def addwork(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and \
                msg.content.lower()[0] in string.printable

        await ctx.send(f"{ctx.author.mention}, please enter the job this work is for")
        question = await self.bot.wait_for("message", check=check)
        user_job = question.content.lower().replace("/", "").replace(".", "").replace("~", "").replace("\"", "").replace("'", "").replace("\\", "").replace("-", "").replace("$", "").replace("{", "").replace("}", "").replace(
            "#", "").replace("?", "").replace("*", "").replace("[", "").replace("]", "").replace(";", "").replace("&", "").replace(">", "").replace("<", "").replace("|", "").replace("!", "").replace("(", "").replace(")", "")
        try:
            with open(f'work/{user_job}.json') as f:
                work_data = json.load(f)
        except FileNotFoundError:
            with open(f'work/jobs.json') as f:
                job_data = json.load(f)
            await ctx.send(f"{ctx.author.mention}, new job detected! Please enter a base salary for this job (just the number). Keep in mind, the base salary for most jobs is around 10.")
            salary = await self.bot.wait_for("message", check=check)
            try:
                job_data.append({
                    "name": user_job,
                    "base_salary": int(salary.content)
                })
            except ValueError:
                await ctx.send("Inputted base salary could not be converted to an integer. Exiting.")
                return 0
            with open(f'work/jobs.json', 'w') as json_file:
                json.dump(job_data, json_file)
            os.system(f'touch work/{user_job}.json')
            work_data = []
        await ctx.send(f"{ctx.author.mention}, please enter the category of this work (reverse, fill in, retype)")
        category = await self.bot.wait_for("message", check=check)
        if(category.content.lower() not in ['reverse', 'fill in', 'retype']):
            await ctx.send("Invalid category. Exiting. If you think this is an error, please ping Max.")
            return 0
        else:
            category = category.content.lower()
        if(category == 'retype'):
            await ctx.send(f"{ctx.author.mention}, please enter the word you would like to be retyped.")
            retype = await self.bot.wait_for("message", check=check)
            work_data.append({"type": "Retype", "desc": "Retype the word below.",
                             "prompt": retype.content, "answer": retype.content})
        elif(category == 'reverse'):
            await ctx.send(f"{ctx.author.mention}, please enter the word you would like to be reversed.")
            retype = await self.bot.wait_for("message", check=check)
            work_data.append({"type": "Reverse", "desc": "Reverse the word below.",
                             "prompt": retype.content, "answer": retype.content[::-1]})
        elif(category == 'fill in'):
            await ctx.send(f"{ctx.author.mention}, please enter the phrase you want to be filled in. Make sure to replace the word you want to be filled in with underscores ( _ ) with spaces in between them signifying how many letters the word you want to be filled in has. (Ex. How _ _ _ you?)")
            retype = await self.bot.wait_for("message", check=check)
            await ctx.send(f"{ctx.author.mention}, please enter the word that should be filled into the above phrase.")
            answer = await self.bot.wait_for("message", check=check)
            work_data.append({"type": "Retype", "desc": "Retype the word below.",
                             "prompt": retype.content, "answer": answer.content})
        with open(f'work/{user_job}.json', 'w') as json_file:
            json.dump(work_data, json_file)
        await ctx.send(f"{ctx.author.mention}, your work was successfully added!")

    @commands.command(name="transfer", help="transfer money to someone else!", aliases=['send', 'share'], pass_context=True)
    async def transfer(self, ctx, member: discord.Member, money: int = None):
        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and \
                msg.content.lower()[0] in string.digits
        with open('profiles.json') as f:
            profile_data = json.load(f)
        found = 0
        uid = member.id
        if member.id == ctx.author.id:
            await ctx.send("You can't transfer money to yourself!")
            return
        if money is None:
            await ctx.send("How much money would you like to transfer to this person?")
            money = await self.bot.wait_for("message", check=check)
            money = int(money.content)
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == ctx.author.id):
                self_index = i
                if(money > profile_data[self_index]['Balance']):
                    await ctx.send("You don't have that much money!")
                    return
                elif(money < 0):
                    await ctx.send("Infinite robux hack does not work on this bot lol")
                    return
                break
        else:
            await ctx.send("How can you transfer money when you don't have any?")
            return
        for i in range(len(profile_data)):
            user_mention = f"<@!{profile_data[i]['ID']}>"
            if(profile_data[i]['ID'] == uid or profile_data[i]['Name'] == uid or profile_data[i]['Nick'] == uid or profile_data[i]['Tag'] == uid or user_mention == uid):
                found = 1
                embedVar = discord.Embed(
                    title=f"Money Transfer to {member.display_name}", timestamp=datetime.utcnow(), color=0xFFFF33)
                embedVar.add_field(
                    name=f"{ctx.author.display_name}", value=f"Old balance: {profile_data[self_index]['Balance']}\nNew balance: {profile_data[self_index]['Balance'] - money}", inline=True)
                profile_data[self_index]['Balance'] = profile_data[self_index]['Balance'] - money
                embedVar.add_field(
                    name=f"{member.display_name}", value=f"Old balance: {profile_data[i]['Balance']}\nNew balance: {profile_data[i]['Balance'] + money}", inline=True)
                profile_data[i]['Balance'] = profile_data[i]['Balance'] + money
                await ctx.reply(embed=embedVar)
        if(found == 0):
            await ctx.send("No profile found for this user! Ask them to create one before transferring money!")
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    @commands.command(name="addmoney", help="add money to someone's profile!", pass_context=True)
    @has_permissions(administrator=True)
    async def addmoney(self, ctx, member: discord.Member, money: int = None):
        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and \
                msg.content.lower()[0] in string.digits
        with open('profiles.json') as f:
            profile_data = json.load(f)
        found = 0
        uid = member.id
        if money is None:
            await ctx.send("How much money would you like to give to this person?")
            money = await self.bot.wait_for("message", check=check)
            money = int(money.content)
        if(money < 0):
            await ctx.send("Infinite robux hack does not work on this bot lol")
            return
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == uid):
                found = 1
                embedVar = discord.Embed(
                    title=f"Giving money to {member.display_name}", timestamp=datetime.utcnow(), color=0x00FF00)
                embedVar.add_field(
                    name=f"{member.display_name}", value=f"Old balance: {profile_data[i]['Balance']}\nNew balance: {profile_data[i]['Balance'] + money}", inline=True)
                profile_data[i]['Balance'] = profile_data[i]['Balance'] + money
                await ctx.reply(embed=embedVar)
        if(found == 0):
            await ctx.send("No profile found for this user! Ask them to create one before giving them money!")
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    @commands.command(name="takemoney", help="take money from someone's profile!", pass_context=True)
    @has_permissions(administrator=True)
    async def takemoney(self, ctx, member: discord.Member, money: int = None):
        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and \
                msg.content.lower()[0] in string.digits
        with open('profiles.json') as f:
            profile_data = json.load(f)
        found = 0
        uid = member.id
        if money is None:
            await ctx.send("How much money would you like to take from this person?")
            money = await self.bot.wait_for("message", check=check)
            money = int(money.content)
        if(money < 0):
            await ctx.send("Infinite robux hack does not work on this bot lol")
            return
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == uid):
                found = 1
                embedVar = discord.Embed(
                    title=f"Removing money from {member.display_name}", timestamp=datetime.utcnow(), color=0xFF0000)
                old_money = profile_data[i]['Balance'] - money
                embedVar.add_field(
                    name=f"{member.display_name}", value=f"Old balance: {profile_data[i]['Balance']}\nNew balance: {profile_data[i]['Balance'] - money}", inline=True)
                profile_data[i]['Balance'] = profile_data[i]['Balance'] - money
                await ctx.reply(embed=embedVar)
        if(found == 0):
            await ctx.send("No profile found for this user! Ask them to create one before ruining their life!")
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    async def cog_command_error(self, ctx, error):
        if not isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")


def setup(bot):
    bot.add_cog(Currency(bot))
