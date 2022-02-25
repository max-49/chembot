import os
import json
import math
import string
import asyncio
import discord
import random
from config import get_bot
from random import randint
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import has_permissions


class Currency(commands.Cog):
    def __init__(self, bot):
        self.info = get_bot(os.getcwd().split('/')[-1])
        self.bot = bot

    @commands.command(name="balance", aliases=['bal', 'money'], help="displays your balance!", pass_context=True)
    async def bal(self, ctx, profile: discord.Member=None):
        with open('profiles.json') as f:
            profile_data = json.load(f)
        if profile is None:
            uid = ctx.author.id
        else:
            uid = profile.id
        found = 0
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == uid):
                found = 1
                embed = discord.Embed(
                    title=f"{profile_data[i]['Name']}'s balance", timestamp=datetime.utcnow(), color=0x00C3FF)
                embed.add_field(
                    name="Balance", value=f"{profile_data[i]['Balance']} {self.info[2]}", inline=False)
                await ctx.reply(embed=embed)
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
                return msg.author.id == 427832149173862400 and msg.channel == ctx.channel
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
                embed = discord.Embed(
                    title="Currently Available Jobs", timestamp=datetime.utcnow(), color=0x00C3FF)
                msg = ""
                for i in range(len(jobs)):
                    msg += f"{jobs[i]['name']}: {jobs[i]['base_salary']} {self.info[2]}\n"
                embed.add_field(name="Jobs", value=msg, inline=False)
                embed.add_field(
                    name="\u200b", value=f"Do `{self.info[3]}work <job>` to select a job!")
                await ctx.reply(embed=embed)
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
                            return
                        else:
                            await ctx.reply(f"You're already working as a {profiles[i]['Job']}! Please do `{self.info[3]}work resign` to choose a new job.")
                            self.work.reset_cooldown(ctx)
                            return
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
            pass
        for i in range(len(profiles)):
            if(profiles[i]['ID'] == ctx.author.id):
                if(profiles[i]['Job'] == ""):
                    await ctx.reply(f"You don't have a job yet! Please choose one at `{self.info[3]}work list`")
                    self.work.reset_cooldown(ctx)
                    return 0
                else:
                    # check for promotion
                    if(profiles[i]['xp'] > (100 + (profiles[i]['level'] * 1.5))):
                        embed = discord.Embed(
                            title="Promotion!", timestamp=datetime.utcnow(), color=0xFFC0CB)
                        embed.add_field(name=f"Congratulations {ctx.author.name}! You've been working hard recently and have worked your way up to a promotion!",
                                           value=f"Level: **{profiles[i]['level']}** --> **{profiles[i]['level'] + 1}**\nSalary: **{profiles[i]['Salary']} {self.info[2]}** --> **{math.floor(profiles[i]['Salary'] * 1.5)} {self.info[2]}**")
                        profiles[i]['level'] += 1
                        profiles[i]['xp'] = 0
                        profiles[i]['Salary'] = math.floor(
                            profiles[i]['Salary'] * 1.5)
                        await ctx.reply(embed=embed)
                        self.work.reset_cooldown(ctx)
                        with open('profiles.json', 'w') as json_file:
                            json.dump(profiles, json_file)
                        return 0
                    with open(f"work/{profiles[i]['Job']}.json") as f:
                        work_scens = json.load(f)
                    scen = randint(0, len(work_scens)-1)
                    embed = discord.Embed(
                        title=f"Work as a {profiles[i]['Job']}", color=0x00C3FF)
                    embed.add_field(
                        name=f"**{work_scens[scen]['type']}** - {work_scens[scen]['desc']}", value=f"`{work_scens[scen]['prompt']}`")
                    await ctx.reply(embed=embed)
                    attempts = 2

                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel
                    while True:
                        try:
                            msg = await self.bot.wait_for("message", check=check, timeout=120)
                        except asyncio.TimeoutError:
                            await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!")
                            break
                        if msg.content.lower() == str(work_scens[scen]['answer']).lower():
                            correct_embed = discord.Embed(color=0x00FF00)
                            correct_embed.add_field(
                                name="Nice job!", value=f"You've earned {profiles[i]['Salary']} {self.info[2]} for working!")
                            profiles[i]['Balance'] += profiles[i]['Salary']
                            xp_given = randint(0, 20)
                            profiles[i]['xp'] += xp_given
                            await msg.reply(embed=correct_embed)
                            break
                        else:
                            if(attempts != 0):
                                await msg.reply(f"Incorrect answer. You have {attempts} attempts left")
                                attempts -= 1
                            else:
                                profiles[i]['Balance'] += math.floor(
                                    int(profiles[i]['Salary'])/3)
                                await msg.reply(f"Incorrect Answer. The correct answer was `{work_scens[scen]['answer']}`. You've earned {math.floor(int(profiles[i]['Salary'])/3)} {self.info[2]} for working.")
                                break
                with open('profiles.json', 'w') as json_file:
                    json.dump(profiles, json_file)
                return
        await ctx.reply(f"You don't have a profile yet! Do `{self.info[3]}profile` to create a profile and start working!")
        self.work.reset_cooldown(ctx)

    @work.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cd = round(error.retry_after)
            minutes = str(cd // 60)
            seconds = str(cd % 60)
            em = discord.Embed(title=f"You can only work once per 5 minutes!", description=f"Try again in {minutes} minutes and {seconds} seconds.", color=0xFF0000)
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
        embed = discord.Embed(
            title="Currently Available Jobs", timestamp=datetime.utcnow(), color=0x00C3FF)
        msg = ""
        for i in range(len(jobs)):
            msg += f"{jobs[i]['name']}: {jobs[i]['base_salary']} {self.info[2]}\n"
        embed.add_field(name="Jobs", value=msg, inline=False)
        embed.add_field(
            name="\u200b", value=f"Do `{self.info[3]}work <job>` to select a job!")
        await ctx.reply(embed=embed)

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
            return msg.author == ctx.author and msg.channel == ctx.channel and \
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
            if int(salary.content) <= 0:
                await ctx.send("You can't have a salary this low! Exiting.")
                return
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
            work_data.append({"type": "Retype", "desc": "Retype the word below.", "prompt": retype.content, "answer": retype.content})
        elif(category == 'reverse'):
            await ctx.send(f"{ctx.author.mention}, please enter the word you would like to be reversed.")
            retype = await self.bot.wait_for("message", check=check)
            work_data.append({"type": "Reverse", "desc": "Reverse the word below.", "prompt": retype.content, "answer": retype.content[::-1]})
        elif(category == 'fill in'):
            await ctx.send(f"{ctx.author.mention}, please enter the phrase you want to be filled in. Make sure to replace the word you want to be filled in with underscores ( `_` ) with spaces in between them signifying how many letters the word you want to be filled in has. (Ex. `How _ _ _ you?`)")
            retype = await self.bot.wait_for("message", check=check)
            await ctx.send(f"{ctx.author.mention}, please enter the word that should be filled into the above phrase.")
            answer = await self.bot.wait_for("message", check=check)
            work_data.append({"type": "Retype", "desc": "Retype the word below.", "prompt": retype.content, "answer": answer.content})
        with open(f'work/{user_job}.json', 'w') as json_file:
            json.dump(work_data, json_file)
        await ctx.send(f"{ctx.author.mention}, your work was successfully added!")

    @commands.command(name="transfer", help="transfer money to someone else!", aliases=['send', 'share'], pass_context=True)
    async def transfer(self, ctx, member: discord.Member, money: int):
        with open('profiles.json') as f:
            profile_data = json.load(f)
        found = 0
        uid = member.id
        if member.id == ctx.author.id:
            await ctx.send("You can't transfer money to yourself!")
            return
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
                embed = discord.Embed(
                    title=f"Money Transfer to {member.display_name}", timestamp=datetime.utcnow(), color=0xFFFF33)
                embed.add_field(
                    name=f"{ctx.author.display_name}", value=f"Old balance: {profile_data[self_index]['Balance']}\nNew balance: {profile_data[self_index]['Balance'] - money}", inline=True)
                profile_data[self_index]['Balance'] = profile_data[self_index]['Balance'] - money
                embed.add_field(
                    name=f"{member.display_name}", value=f"Old balance: {profile_data[i]['Balance']}\nNew balance: {profile_data[i]['Balance'] + money}", inline=True)
                profile_data[i]['Balance'] = profile_data[i]['Balance'] + money
                await ctx.reply(embed=embed)
        if(found == 0):
            await ctx.send("No profile found for this user! Ask them to create one before transferring money!")
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    @commands.command(name="addmoney", help="add money to someone's profile!", pass_context=True)
    @has_permissions(administrator=True)
    async def addmoney(self, ctx, member: discord.Member, money: int = None):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and \
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
                embed = discord.Embed(
                    title=f"Giving money to {member.display_name}", timestamp=datetime.utcnow(), color=0x00FF00)
                embed.add_field(
                    name=f"{member.display_name}", value=f"Old balance: {profile_data[i]['Balance']}\nNew balance: {profile_data[i]['Balance'] + money}", inline=True)
                profile_data[i]['Balance'] = profile_data[i]['Balance'] + money
                await ctx.reply(embed=embed)
        if(found == 0):
            await ctx.send("No profile found for this user! Ask them to create one before giving them money!")
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    @commands.command(name="takemoney", help="take money from someone's profile!", pass_context=True)
    @has_permissions(administrator=True)
    async def takemoney(self, ctx, member: discord.Member, money: int = None):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and \
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
                embed = discord.Embed(
                    title=f"Removing money from {member.display_name}", timestamp=datetime.utcnow(), color=0xFF0000)
                embed.add_field(
                    name=f"{member.display_name}", value=f"Old balance: {profile_data[i]['Balance']}\nNew balance: {profile_data[i]['Balance'] - money}", inline=True)
                profile_data[i]['Balance'] = profile_data[i]['Balance'] - money
                await ctx.reply(embed=embed)
        if(found == 0):
            await ctx.send("No profile found for this user! Ask them to create one before ruining their life!")
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    @commands.command(name='table', help='shows the slots payout table!')
    async def table(self, ctx):
        tables = [ { 'emoji': '⚽️', 'count': 2, 'payout': 1 }, { 'emoji': '🔍', 'count': 2, 'payout': 1 }, { 'emoji': '⌛️', 'count': 2, 'payout': 1.75 }, { 'emoji': '🏓', 'count': 2, 'payout': 1.75 }, { 'emoji': '🔴', 'count': 2, 'payout': 2 }, { 'emoji': '🌍', 'count': 2, 'payout': 2 }, { 'emoji': '💵', 'count': 2, 'payout': 2 }, { 'emoji': '📸', 'count': 2, 'payout': 2 }, { 'emoji': '🏓', 'count': 3, 'payout': 5 }, { 'emoji': '⚽️', 'count': 3, 'payout': 10 }, { 'emoji': '🔍', 'count': 3, 'payout': 10 }, { 'emoji': '🔴', 'count': 3, 'payout': 20 }, { 'emoji': '⌛️', 'count': 3, 'payout': 25 }, { 'emoji': '🌍', 'count': 3, 'payout': 50 }, { 'emoji': '📸', 'count': 3, 'payout': 75 }, { 'emoji': '💵', 'count': 3, 'payout': 250 }]
        emojis = ''
        for table in tables:
            emojis += f"{table['emoji'] * table['count']}     - {table['payout']}x\n"
        embed = discord.Embed(title='Slots payout table!', timestamp=datetime.utcnow(), color=0x00C3FF)
        embed.add_field(name='emoji - payout', value=emojis, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='shop', help='buy items at the shop!')
    async def shop(self, ctx):
        embed = discord.Embed(title='BagelBot shop!', timestamp=datetime.utcnow(), color=0x00C3FF)
        embed.add_field(name='Items for sale! (Item code - Price)', value='**1kbagels** - 1,000 bagels\n**fakeflag** - 1,000 bagels\n**flag** - 1,000,000 bagels', inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='buy', help='buy an item from the shop!')
    async def buy(self, ctx, buy_item: str):
        with open('profiles.json') as f:
            profile_data = json.load(f)
        items = [{'name': '1kbagels', 'price': 1000}, {'name': 'fakeflag', 'price': 1000}, {'name': 'flag', 'price': 1000000}]
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == ctx.author.id):        
                for item in items:
                    if(item['name'] == buy_item):
                        if(item['price'] > profile_data[i]['Balance']):
                            await ctx.reply("You don't have enough money to buy this item!")
                            return
                        else:
                            profile_data[i]['Balance'] = profile_data[i]['Balance'] - item['price']
                            if(item['name'] == '1kbagels'):
                                profile_data[i]['Balance'] = profile_data[i]['Balance'] + 1000
                                await ctx.reply('1,000 bagels have been accredited to your account!')
                            elif(item['name'] == 'fakeflag'):
                                await ctx.reply("this flag is so fake")
                            elif(item['name'] == 'flag'):
                                await ctx.reply("here's a random number" + str(random.randint(0,12033131231231)))
                            else:
                                await ctx.reply("i have no idea how you got here. dm max if you got here.")
                            with open('profiles.json', 'w') as json_file:
                                json.dump(profile_data, json_file)
                            return
                await ctx.reply(f"Item doesn't exist! Make sure to use the item code found in `{self.info[3]}shop`")
                return
        await ctx.reply(f"You don't have a profile yet! Create one with `{self.info[3]}balance`!")

    @commands.command(name='high', help='roll the higher number to win!')
    async def high(self, ctx, amount: int):
        await ctx.invoke(self.bet, 'high', amount)

    @commands.command(name='slots', help='slot machine!')
    async def slots(self, ctx, amount: int):
        await ctx.invoke(self.bet, 'slots', amount)

    @commands.command(name="bet", help="bet <high | slots> <amount>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bet(self, ctx, bet: str, amount: int):
        with open('profiles.json') as f:
            profile_data = json.load(f)
        if(amount < 0):
            await ctx.reply('no')
            return
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == ctx.author.id):
                original_balance = int(profile_data[i]['Balance'])
                if(amount > original_balance):
                    await ctx.reply("You can't bet more than you have!")
                    return
                if(bet == 'high'):
                    welcome_message = f"High - roll a higher number than {self.bot.user.name} to win!"
                    bagel_roll = random.randint(1,6)
                    you_roll = random.randint(1,6)
                    if(you_roll > bagel_roll):
                        embed = discord.Embed(title=welcome_message, timestamp=datetime.utcnow(), color=0x00ff00)
                        embed.add_field(name='BagelBot rolls...', value=bagel_roll, inline=True)
                        embed.add_field(name='You roll...', value=you_roll, inline=True)
                        embed.add_field(name=f'Congrats, you win! Your new balance is {math.floor(original_balance + amount)} {self.info[2]}!', value=f':)', inline=False)
                        profile_data[i]['Times'] = profile_data[i]['Times'] + 1
                        profile_data[i]['Win'] = profile_data[i]['Win'] + 1
                        profile_data[i]['Profit'] = profile_data[i]['Profit'] + math.floor(amount)
                        profile_data[i]['Balance'] = int(math.floor(original_balance + (amount)))
                        await ctx.reply(embed=embed)
                    elif(you_roll < bagel_roll):
                        embed = discord.Embed(title=welcome_message, timestamp=datetime.utcnow(), color=0xFF0000)
                        embed.add_field(name='BagelBot rolls...', value=bagel_roll, inline=True)
                        embed.add_field(name='You roll...', value=you_roll, inline=True)
                        profile_data[i]['Times'] = profile_data[i]['Times'] + 1
                        profile_data[i]['Lose'] = profile_data[i]['Lose'] + 1
                        profile_data[i]['Profit'] = profile_data[i]['Profit'] - amount
                        embed.add_field(name=f'You lose! Your new balance is {original_balance - amount} {self.info[2]}!', value=':(', inline=False)
                        profile_data[i]['Balance'] = int(original_balance - amount)
                        await ctx.reply(embed=embed)
                    else:
                        embed = discord.Embed(title=welcome_message, timestamp=datetime.utcnow(), color=0xFFFF00)
                        embed.add_field(name='BagelBot rolls...', value=bagel_roll, inline=True)
                        embed.add_field(name='You roll...', value=you_roll, inline=True)
                        embed.add_field(name=f'Tie! Nobody loses money!', value='Close one', inline=False)
                        profile_data[i]['Times'] = profile_data[i]['Times'] + 1
                        await ctx.reply(embed=embed)
                elif(bet == 'slots'):
                    welcome_message = f"Slots - payout table is at {self.info[3]}table!"
                    emojis = ['⚽️', '🔴', '🔍', '🌍', '📸', '💵', '⌛️', '🏓']
                    slots = ' '.join([random.choice(emojis), random.choice(emojis), random.choice(emojis)])
                    tables = [ { 'emoji': '⚽️', 'count': 2, 'payout': 1 }, { 'emoji': '🔍', 'count': 2, 'payout': 1 }, { 'emoji': '⌛️', 'count': 2, 'payout': 1.75 }, { 'emoji': '🏓', 'count': 2, 'payout': 1.75 }, { 'emoji': '🔴', 'count': 2, 'payout': 2 }, { 'emoji': '🌍', 'count': 2, 'payout': 2 }, { 'emoji': '💵', 'count': 2, 'payout': 2 }, { 'emoji': '📸', 'count': 2, 'payout': 2 }, { 'emoji': '🏓', 'count': 3, 'payout': 5 }, { 'emoji': '⚽️', 'count': 3, 'payout': 10 }, { 'emoji': '🔍', 'count': 3, 'payout': 10 }, { 'emoji': '🔴', 'count': 3, 'payout': 20 }, { 'emoji': '⌛️', 'count': 3, 'payout': 25 }, { 'emoji': '🌍', 'count': 3, 'payout': 50 }, { 'emoji': '📸', 'count': 3, 'payout': 75 }, { 'emoji': '💵', 'count': 3, 'payout': 250 }]
                    payout = 0
                    for emoji in emojis:
                        instances = slots.count(emoji)
                        for table in tables:
                            if(emoji == table['emoji'] and instances == table['count']):
                                payout = table['payout']
                    if(payout == 0):
                        embed = discord.Embed(title=welcome_message, timestamp=datetime.utcnow(), color=0xFF0000)
                        embed.add_field(name='Your slot roll:', value=f'**>** {slots} **<**', inline=False)
                        embed.add_field(name=f'You lose! Your new balance is {original_balance - amount} {self.info[2]}.', value=':(', inline=False)
                        profile_data[i]['Times'] = profile_data[i]['Times'] + 1
                        profile_data[i]['Lose'] = profile_data[i]['Lose'] + 1
                        profile_data[i]['Profit'] = profile_data[i]['Profit'] - amount
                        profile_data[i]['Balance'] = original_balance - amount
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title=welcome_message, timestamp=datetime.utcnow(), color=0x00FF00)
                        embed.add_field(name='Your slot roll:', value=f'**>** {slots} **<**', inline=False)
                        embed.add_field(name=f'You win! Your new balance is {math.floor(original_balance + (amount * payout))} {self.info[2]}! ({payout}x payout)', value=':)', inline=False)
                        profile_data[i]['Times'] = profile_data[i]['Times'] + 1
                        profile_data[i]['Win'] = profile_data[i]['Win'] + 1
                        profile_data[i]['Profit'] = profile_data[i]['Profit'] + math.floor(amount * payout)
                        profile_data[i]['Balance'] = math.floor(original_balance + (amount * payout))
                        await ctx.send(embed=embed)
                else:
                    await ctx.reply('Invalid option! Please choose either `high` or `slots`.')
                    return
                with open('profiles.json', 'w') as json_file:
                    json.dump(profile_data, json_file)
                return
        await ctx.send(f"You don't have a profile yet! Do `{self.info[3]}balance` to create one!")
        self.bet.reset_cooldown(ctx)

    @bet.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cd = round(error.retry_after)
            seconds = str(cd % 60)
            em = discord.Embed(title=f"Woah! Stop betting so fast!", description=f"Try again in {seconds} seconds.", color=0xFF0000)
            await ctx.send(embed=em)


    @commands.command(name='beg', help="beg for money because you don't have any")
    @commands.cooldown(1, 240, commands.BucketType.user)
    async def beg(self, ctx):
        choice = random.randint(0,1)
        if(choice == 0):
            embed = discord.Embed(title='Begging', timestamp=datetime.utcnow(), color=0xFF0000)
            embed.add_field(name='Your begging did not work', value='No extra money for you', inline=False)
            await ctx.send(embed=embed)
        else:
            with open('profiles.json') as f:
                profile_data = json.load(f)
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == ctx.author.id):
                    original_balance = int(profile_data[i]['Balance'])
                    money = random.randint(50, 200)
                    embed = discord.Embed(title='Begging', timestamp=datetime.utcnow(), color=0x00FF00)
                    embed.add_field(name=f"Your begging worked and you've received {money} {self.info[2]}!", value=f'Your balance is now {original_balance + money}', inline=False)
                    profile_data[i]['Balance'] = profile_data[i]['Balance'] + money
                    await ctx.send(embed=embed)
                    with open('profiles.json', 'w') as json_file:
                        json.dump(profile_data, json_file)
                    return
            await ctx.send(f"You don't have a profile yet! Do `{self.info[3]}balance` to create one.")
            self.beg.reset_cooldown(ctx)
            

    @beg.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cd = round(error.retry_after)
            minutes = str(cd // 60)
            seconds = str(cd % 60)
            em = discord.Embed(title=f"You can't just keep begging to get money!", description=f"Try again in {minutes} minutes and {seconds} seconds.", color=0xFF0000)
            await ctx.send(embed=em)

    @commands.command(name="sim", help="sim <high | slots> <amount> <times>")
    async def sim(self, ctx, bet: str, amount: int, times: int):
        if(times < 1):
            await ctx.reply('You can\'t simulate that number of attempts!')
            return
        if(amount < 0):
            await ctx.reply('You can\'t bet a negative amount of money!')
            return
        if(bet not in ["high", "slots"]):
            await ctx.reply("You can only simulate 'high' or 'slots'!")
            return
        if(times > 10000):
            await ctx.reply("You can't simulate more than 10000 attempts (for now)!")
            return
        if(amount > 1000000):
            await ctx.reply("You can't simulate bets of more than 1,000,000 bagels (for now)!")
            return
        if(bet == 'high'):
            times_won = 0
            times_tied = 0
            times_lost = 0
            net_profit = 0
            for _ in range(times):
                bagel_roll = random.randint(1,6)
                you_roll = random.randint(1,6)
                if(you_roll > bagel_roll):
                    times_won += 1
                    net_profit += amount
                elif(you_roll < bagel_roll):
                    times_lost += 1
                    net_profit -= amount
                else:
                    times_tied += 1
            embed = discord.Embed(title=f"{self.bot.user.name} High Simulation", timestamp=datetime.utcnow(), color=0x00FF00)
            embed.add_field(name='Times won', value=f"{times_won}/{times} ({round((times_won/times)*100, 2)}%)")
            embed.add_field(name='Times tied', value=f"{times_tied}/{times} ({round((times_tied/times)*100, 2)}%)")
            embed.add_field(name='Times lost', value=f"{times_lost}/{times} ({round((times_lost/times)*100, 2)}%)")
            embed.add_field(name='Net profit with consistent bet of {:,} {}'.format(amount, self.info[2]), value="{:,}".format(net_profit), inline=False)
            await ctx.reply(embed=embed)
        elif(bet == 'slots'):
            emojis = ['⚽️', '🔴', '🔍', '🌍', '📸', '💵', '⌛️', '🏓']
            tables = [ { 'emoji': '⚽️', 'count': 2, 'payout': 1 }, { 'emoji': '🔍', 'count': 2, 'payout': 1 }, { 'emoji': '⌛️', 'count': 2, 'payout': 1.75 }, { 'emoji': '🏓', 'count': 2, 'payout': 1.75 }, { 'emoji': '🔴', 'count': 2, 'payout': 2 }, { 'emoji': '🌍', 'count': 2, 'payout': 2 }, { 'emoji': '💵', 'count': 2, 'payout': 2 }, { 'emoji': '📸', 'count': 2, 'payout': 2 }, { 'emoji': '🏓', 'count': 3, 'payout': 5 }, { 'emoji': '⚽️', 'count': 3, 'payout': 10 }, { 'emoji': '🔍', 'count': 3, 'payout': 10 }, { 'emoji': '🔴', 'count': 3, 'payout': 20 }, { 'emoji': '⌛️', 'count': 3, 'payout': 25 }, { 'emoji': '🌍', 'count': 3, 'payout': 50 }, { 'emoji': '📸', 'count': 3, 'payout': 75 }, { 'emoji': '💵', 'count': 3, 'payout': 250 }]
            times_won = 0
            times_lost = 0
            net_profit = 0
            for _ in range(times):
                slots = ' '.join([random.choice(emojis), random.choice(emojis), random.choice(emojis)])     
                payout = 0
                for emoji in emojis:
                    instances = slots.count(emoji)
                    for table in tables:
                        if(emoji == table['emoji'] and instances == table['count']):
                            payout = table['payout']
                if(payout == 0):
                    times_lost += 1
                    net_profit -= amount
                else:
                    times_won += 1
                    net_profit += math.floor(amount * payout)
            embed = discord.Embed(title=f"{self.user.bot.name} Slots Simulation", timestamp=datetime.utcnow(), color=0x00FF00)
            embed.add_field(name='Times won', value=f"{times_won}/{times} ({round((times_won/times)*100, 2)}%)")
            embed.add_field(name='Times lost', value=f"{times_lost}/{times} ({round((times_lost/times)*100, 2)}%)")
            embed.add_field(name='Net profit with consistent bet of {:,} {}'.format(amount, self.info[2]), value="{:,}".format(net_profit), inline=False)
            await ctx.reply(embed=embed)

    async def cog_command_error(self, ctx, error):
        if not isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")


def setup(bot):
    bot.add_cog(Currency(bot))
