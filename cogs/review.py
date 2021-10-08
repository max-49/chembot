import os
import json
import discord
import asyncio
import itertools
from config import get_bot
from random import randint, choice
from datetime import datetime
from discord.ext import commands

class Regents(discord.ui.View):
    def __init__(self, correct: str, category: str):
        super().__init__()
        self.value = None
        self.correct = correct
        self.category = category

    @discord.ui.button(label='a', style=discord.ButtonStyle.grey)
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
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label='b', style=discord.ButtonStyle.grey)
    async def b(self, button: discord.ui.Button, interaction: discord.Interaction):
        if(self.correct == 'b'):
            await interaction.response.send_message('Correct!', ephemeral=True)
            button.style = discord.ButtonStyle.green
            button.disabled = True
            self.value = True
        else:
            await interaction.response.send_message(f'Incorrect! The correct answer was {self.correct}. You should probably review the {self.category} unit.', ephemeral=True)
            button.style = discord.ButtonStyle.red
            button.disabled = True
            self.value = False
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label='c', style=discord.ButtonStyle.grey)
    async def c(self, button: discord.ui.Button, interaction: discord.Interaction):
        if(self.correct == 'c'):
            await interaction.response.send_message('Correct!', ephemeral=True)
            button.style = discord.ButtonStyle.green
            button.disabled = True
            self.value = True       
        else:
            await interaction.response.send_message(f'Incorrect! The correct answer was {self.correct}. You should probably review the {self.category} unit.', ephemeral=True)
            button.style = discord.ButtonStyle.red
            button.disabled = True
            self.value = False           
        await interaction.response.edit_message(view=self)
        self.stop()
    
    @discord.ui.button(label='d', style=discord.ButtonStyle.grey)
    async def d(self, button: discord.ui.Button, interaction: discord.Interaction):
        if(self.correct == 'd'):
            await interaction.response.send_message('Correct!', ephemeral=True)
            button.style = discord.ButtonStyle.green
            button.disabled = True
            self.value = True           
        else:
            await interaction.response.send_message(f'Incorrect! The correct answer was {self.correct}. You should probably review the {self.category} unit.', ephemeral=True)
            button.style = discord.ButtonStyle.red
            button.disabled = True
            self.value = False    
        await interaction.response.edit_message(view=self)
        self.stop()

class Review(commands.Cog):
    def __init__(self, bot):
        self.info = get_bot(os.getcwd().split('/')[-1])
        self.bot = bot

    @commands.command(name='profile', help="displays your profile", pass_context=True)
    async def profile(self, ctx, profile: discord.Member=None):
        while True:
            try:
                with open(f'profiles.json') as f:
                    profile_data = json.load(f)
                break
            except FileNotFoundError:
                with open(f'profiles.json', 'w') as f:
                    f.write('[]')
                continue
        
        uid = ctx.author.id if profile is None else profile.id
        if(len(profile_data) == 0):
            if profile is None:
                profile = ctx.author
            profile_data.append({"Name": profile.name, "Tag": str(profile), "Nick": profile.display_name, "ID": profile.id, "Avatar URL": str(
                profile.avatar.url), "Correct": 0, "Total": 0, "Calc": True, "Table": True, "WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1, "Times": 0, "Win": 0, "Lose": 0, "Profit": 0})
            embedVar = discord.Embed(
                title=f"{profile.name}'s profile",  timestamp=datetime.utcnow(), color=0x00ff00)
            percent_correct = 0
            embedVar.add_field(name="Profile initialized!", value=f"Run the command again to see your profile!", inline=False)
            embedVar.set_thumbnail(url=profile.avatar.url)
            await ctx.send(embed=embedVar)
            with open(f'profiles.json', 'w') as json_file:
                json.dump(profile_data, json_file)
            return
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == uid):
                embedVar = discord.Embed(
                    title=f"{profile_data[i]['Name']}'s profile",  timestamp=datetime.utcnow(), color=0x00ff00)
                try:
                    percent_correct = (
                        profile_data[i]['Correct']/profile_data[i]['Total']) * 100
                except ZeroDivisionError:
                    percent_correct = 0
                embedVar.add_field(name="Chemistry Regents Review Stats", value=f"{str(profile_data[i]['Correct'])}/{str(profile_data[i]['Total'])} ({str(round(percent_correct, 2))}%)", inline=False)
                embedVar.add_field(
                    name="Balance", value=f"{profile_data[i]['Balance']} {self.info[2]}", inline=False)
                embedVar.add_field(name="Net profit from betting", value=f"{profile_data[i]['Profit']} bagels", inline=False)
                try:
                    percent = round((profile_data[i]['Win']/profile_data[i]['Times'])*100, 2)
                except ZeroDivisionError:
                    percent = 0
                embedVar.add_field(name="Percent times won", value=f"{profile_data[i]['Win']}/{profile_data[i]['Times']} times ({percent}%)", inline=False) 
                embedVar.set_thumbnail(url=profile_data[i]['Avatar URL'])
                await ctx.send(embed=embedVar)
                return
        else:
            if profile is None:
                profile = ctx.author
            profile_data.append({"Name": profile.name, "Tag": str(profile), "Nick": profile.display_name, "ID": profile.id, "Avatar URL": str(
                profile.avatar.url), "Correct": 0, "Total": 0, "Calc": "True", "Table": "True", "WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1, "Times": 0, "Win": 0, "Lose": 0, "Profit": 0})
            embedVar = discord.Embed(
                title=f"{profile.name}'s profile",  timestamp=datetime.utcnow(), color=0x00ff00)
            percent_correct = 0
            embedVar.add_field(name="Profile initialized!", value="Run the command again to see your profile!", inline=False)
            embedVar.set_thumbnail(url=profile.avatar.url)
            await ctx.send(embed=embedVar)
            with open(f'profiles.json', 'w') as json_file:
                json.dump(profile_data, json_file)

    @commands.command(name='regents', help="dispenses a Random regents question (syntax: regents (<atom>, <periodic>, <matter>, <solubility>", pass_context=True)
    async def regents(self, ctx, category: str=None):
        found = 0
        with open(f'profiles.json') as f:
            profile_data = json.load(f)
        self_index = -1
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == ctx.author.id):
                found = 1
                self_index = i
        if(found == 0):
            profile_data.append({"Name": ctx.author.name, "Tag": str(ctx.author), "Nick": ctx.author.display_name, "ID": ctx.author.id, "Avatar URL": str(
                ctx.author.avatar.url), "Correct": 0, "Total": 0, "Calc": True, "Table": True, "WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1, "Times": 0, "Win": 0, "Lose": 0, "Profit": 0})
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == ctx.author.id):
                    found = 1
                    self_index = i
        
        with open('questions/categories.json') as j:
            categories = json.load(j)

        if category is not None:
            if category.lower() in categories:
                category = category.lower()
            else:
                await ctx.reply("Invalid Category! Choosing random category.")
                category = choice(categories)
        else:
            category = choice(categories)

        with open(f'questions/{category.lower()}.json') as j:
            questions = json.load(j)
        while True:
            question_number = randint(0, len(questions)-1)
            if questions[question_number]["Calc"] and not profile_data[self_index]["Calc"]:
                questions.pop(i)
                continue
            if questions[question_number]["Table"] and not profile_data[self_index]["Table"]:
                questions.pop(i)
                continue
            else:
                break

        embedVar = discord.Embed(
            title="Question #" + str(question_number + 1), timestamp=datetime.utcnow(), color=0x00ff00)

        if(questions[question_number]['image'] != 0):
            embedVar.set_image(url=questions[question_number]['image'])

        embedVar.add_field(name=questions[question_number]['question'], value="a) " + str(questions[question_number]['choices'][0]) + "\nb) " + str(
            questions[question_number]['choices'][1]) + "\nc) " + str(questions[question_number]['choices'][2]) + "\nd) " + str(questions[question_number]['choices'][3]), inline=False)

        if(questions[question_number]['Calc'] and questions[question_number]['Table']):
            embedVar.add_field(name="Tools required", value="Calculator and Reference Table", inline=False)
        elif(questions[question_number]['Calc'] and not questions[question_number]['Table']):
            embedVar.add_field(name="Tools required", value="Calculator", inline=False)
        elif(not questions[question_number]['Calc'] and questions[question_number]['Table']):
            embedVar.add_field(name="Tools required", value="Reference Table", inline=False)

        embedVar.add_field(name="Category", value="`" + str(category)+"`", inline=False)

        regents = Regents(questions[question_number]['answer'], category)
        await ctx.reply(embed=embedVar, view=regents)

        await regents.wait()
        if regents.value is None:
            await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!")
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == ctx.author.id):
                    profile_data[i]['Total'] += 1
        elif regents.value:
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == ctx.author.id):
                    profile_data[i]['Correct'] += 1
                    profile_data[i]['Total'] += 1
        else:
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == ctx.author.id):
                    profile_data[i]['Total'] += 1

        # def check(msg):
        #     return msg.author == ctx.author and msg.channel == msg.channel and \
        #         msg.content.lower() in ["a", "b", "c", "d"]
        # try:
        #     msg = await self.bot.wait_for("message", check=check, timeout=90)
        # except asyncio.TimeoutError:
        #     await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!")
        #     for i in range(len(profile_data)):
        #         if(profile_data[i]['ID'] == ctx.author.id):
        #             profile_data[i]['Total'] += 1
        # if msg.content.lower() == questions[question_number]['answer']:
        #     for i in range(len(profile_data)):
        #         if(profile_data[i]['ID'] == ctx.author.id):
        #             profile_data[i]['Correct'] += 1
        #             profile_data[i]['Total'] += 1
        #     await msg.reply("Correct!")
        # else:
        #     for i in range(len(profile_data)):
        #         if(profile_data[i]['ID'] == ctx.author.id):
        #             profile_data[i]['Total'] += 1
        #     await msg.reply(f"Incorrect Answer. The correct answer was `{questions[question_number]['answer']}`.\nYou should probably review the `{category}` unit.")
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    @commands.command(name='leaderboard', help="Displays the global leaderboards", aliases=['lb', 'leader'], pass_context=True)
    async def lb(self, ctx, *, lb: str = None):
        with open('profiles.json') as f:
            profile_data = json.load(f)
        percentages = {}
        if lb is not None:
            if(lb.lower() in ['world', 'chem', 'apworld', 'chemistry', 'bal', 'money', 'rich', 'schlucks', 'coins']):
                if(lb.lower() == 'world' or lb.lower() == 'apworld'):
                    for i in range(len(profile_data)):
                        try:
                            percent_correct = (
                                profile_data[i]['WorldCorrect']/profile_data[i]['WorldTotal']) * 100
                        except ZeroDivisionError:
                            percent_correct = 0
                        percentages[str(profile_data[i]['Name'])
                                    ] = percent_correct
                    embedVar = discord.Embed(
                        title="AP World Leaderboard", timestamp=datetime.utcnow(), color=0x00ff00)
                    sorted_percentages = {k: v for k, v in sorted(
                        percentages.items(), key=lambda item: item[1], reverse=True)}
                    msg = ""
                    place = 1
                    for key in sorted_percentages:
                        msg += str(place) + ". " + key + " (" + \
                            str(round(sorted_percentages[key], 2)) + "%)\n"
                        place += 1
                    embedVar.add_field(name="Placements", value=msg, inline=False)
                    await ctx.send(embed=embedVar)
                elif(lb.lower() == 'bal' or lb.lower() == 'money' or lb.lower() == 'rich' or lb.lower() == 'schlucks'):
                    for i in range(len(profile_data)):
                        try:
                            schlucks = profile_data[i]['Balance']
                        except ZeroDivisionError:
                            schlucks = 0
                        percentages[str(profile_data[i]['Name'])] = schlucks
                    embedVar = discord.Embed(
                        title="Richest Users", timestamp=datetime.utcnow(), color=0x00ff00)
                    sorted_percentages = {k: v for k, v in sorted(
                        percentages.items(), key=lambda item: item[1], reverse=True)}
                    msg = ""
                    place = 1
                    for key in sorted_percentages:
                        msg += str(place) + ". " + key + " (" + \
                            str(round(
                                sorted_percentages[key], 2)) + " schlucks)\n"
                        place += 1
                    embedVar.add_field(name="Placements", value=msg, inline=False)
                    await ctx.send(embed=embedVar)
                else:
                    for i in range(len(profile_data)):
                        try:
                            percent_correct = (
                                profile_data[i]['Correct']/profile_data[i]['Total']) * 100
                        except ZeroDivisionError:
                            percent_correct = 0
                        percentages[str(profile_data[i]['Name'])
                                    ] = percent_correct
                    embedVar = discord.Embed(
                        title="Chemistry Leaderboard", timestamp=datetime.utcnow(), color=0x00ff00)
                    sorted_percentages = {k: v for k, v in sorted(
                        percentages.items(), key=lambda item: item[1], reverse=True)}
                    msg = ""
                    place = 1
                    for key in sorted_percentages:
                        msg += str(place) + ". " + key + " (" + \
                            str(round(sorted_percentages[key], 2)) + "%)\n"
                        place += 1
                    embedVar.add_field(name="Placements", value=msg, inline=False)
                    await ctx.send(embed=embedVar)
            elif(lb.lower() in ['times', 'win', 'lose', 'profit', 'negprofit']):
                if(lb.lower() == 'win' or lb.lower() == 'lose'):
                    if(lb.lower() == 'win'):
                        lb_type = 'Win'
                    else:
                        lb_type = 'Lose'
                    for i in range(len(profile_data)):
                        try:
                            percent_correct = (profile_data[i][lb_type]/profile_data[i]['Times']) * 100
                        except ZeroDivisionError:
                            percent_correct = 0
                        percentages[str(profile_data[i]['Name'])] = percent_correct
                    embedVar = discord.Embed(title=f"Highest {lb_type} Percentages", timestamp=datetime.utcnow(), color=0x00ff00)
                    sorted_percentages = {k: v for k, v in sorted(percentages.items(), key=lambda item: item[1], reverse=True)}
                    msg = ""
                    place = 1
                    if(len(sorted_percentages) < 10):
                        for key in sorted_percentages:
                            msg += str(place) + ". " + key + " (" + \
                                str(round(sorted_percentages[key], 2)) + f"%)\n"
                            place += 1
                    else:
                        for key in itertools.islice(sorted_percentages, 10):
                            msg += str(place) + ". " + key + " (" + \
                                str(round(sorted_percentages[key], 2)) + f"%)\n"
                            place += 1
                    embedVar.add_field(name="Placements", value=msg, inline=False)
                    await ctx.send(embed=embedVar)
                elif(lb.lower() == 'times' or lb.lower() == 'profit' or lb.lower() == 'bagels'):
                    if(lb.lower() == 'times'):
                        lb_type = 'Times'
                        end = 'times'
                        embedVar = discord.Embed(title="People who have gambled the most", timestamp=datetime.utcnow(), color=0x00ff00)
                    elif(lb.lower() == 'profit'):
                        lb_type = 'Profit'
                        end = self.info[2]
                        embedVar = discord.Embed(title="Users who have made the most profit", timestamp=datetime.utcnow(), color=0x00ff00)
                    else:
                        lb_type = 'Balance'
                        end = self.info[2]
                        embedVar = discord.Embed(title="Richest Users", timestamp=datetime.utcnow(), color=0x00ff00)
                    for i in range(len(profile_data)):
                        for i in range(len(profile_data)):
                            number = profile_data[i][lb_type]
                            percentages[str(profile_data[i]['Name'])] = number
                    sorted_percentages = {k: v for k, v in sorted(percentages.items(), key=lambda item: item[1], reverse=True)}
                    msg = ""
                    place = 1
                    if(len(sorted_percentages) < 10):
                        for key in sorted_percentages:
                            msg += str(place) + ". " + key + " (" + \
                                str(round(sorted_percentages[key], 2)) + f" {end})\n"
                            place += 1
                    else:
                        for key in itertools.islice(sorted_percentages, 10):
                            msg += str(place) + ". " + key + " (" + \
                                str(round(sorted_percentages[key], 2)) + f" {end})\n"
                            place += 1

                    embedVar.add_field(name="Placements", value=msg, inline=False)
                    await ctx.send(embed=embedVar)
                elif(lb.lower() == 'negprofit'):
                    embedVar = discord.Embed(title="Users who have made the least profit", timestamp=datetime.utcnow(), color=0x00ff00)
                    for i in range(len(profile_data)):
                        for i in range(len(profile_data)):
                            number = profile_data[i]['Profit']
                            percentages[str(profile_data[i]['Name'])] = number
                    sorted_percentages = {k: v for k, v in sorted(percentages.items(), key=lambda item: item[1], reverse=False)}
                    msg = ""
                    place = 1
                    if(len(sorted_percentages) < 10):
                        for key in sorted_percentages:
                            msg += str(place) + ". " + key + " (" + \
                                str(round(sorted_percentages[key], 2)) + f" bagels)\n"
                            place += 1
                    else:
                        for key in itertools.islice(sorted_percentages, 10):
                            msg += str(place) + ". " + key + " (" + \
                                str(round(sorted_percentages[key], 2)) + f" bagels)\n"
                            place += 1

                    embedVar.add_field(name="Placements", value=msg, inline=False)
                    await ctx.send(embed=embedVar)
            else:
                await ctx.send("Invalid leaderboard choice! Showing chemistry leaderboard")
                for i in range(len(profile_data)):
                    try:
                        percent_correct = (
                            profile_data[i]['Correct']/profile_data[i]['Total']) * 100
                    except ZeroDivisionError:
                        percent_correct = 0
                    percentages[str(profile_data[i]['Name'])] = percent_correct
                embedVar = discord.Embed(
                    title="Chemistry Leaderboard", timestamp=datetime.utcnow(), color=0x00ff00)
                sorted_percentages = {k: v for k, v in sorted(
                    percentages.items(), key=lambda item: item[1], reverse=True)}
                msg = ""
                place = 1
                for key in sorted_percentages:
                    msg += str(place) + ". " + key + " (" + \
                        str(round(sorted_percentages[key], 2)) + "%)\n"
                    place += 1
                embedVar.add_field(name="Placements", value=msg, inline=False)
                await ctx.send(embed=embedVar)
        else:
            for i in range(len(profile_data)):
                try:
                    percent_correct = (
                        profile_data[i]['Correct']/profile_data[i]['Total']) * 100
                except ZeroDivisionError:
                    percent_correct = 0
                percentages[str(profile_data[i]['Name'])] = percent_correct
            embedVar = discord.Embed(
                title="Chemistry Leaderboard", timestamp=datetime.utcnow(), color=0x00ff00)
            sorted_percentages = {k: v for k, v in sorted(
                percentages.items(), key=lambda item: item[1], reverse=True)}
            msg = ""
            place = 1
            for key in sorted_percentages:
                msg += str(place) + ". " + key + " (" + \
                    str(round(sorted_percentages[key], 2)) + "%)\n"
                place += 1
            embedVar.add_field(name="Placements", value=msg, inline=False)
            await ctx.send(embed=embedVar)

    @commands.command(name='settings', help="displays the settings menu")
    async def settings(self, ctx, *params):
        with open('profiles.json') as f:
            profile_data = json.load(f)
        uid = ctx.author.id
        found = 0
        found_indices = []
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == uid):
                found = 1
                found_indices.append(i)
        if(found == 0):
            profile_data.append({"Name": ctx.author.name, "Tag": str(ctx.author), "Nick": ctx.author.display_name, "ID": ctx.author.id, "Avatar URL": str(
                ctx.author.avatar.url), "Correct": 0, "Total": 0, "Calc": True, "Table": True, "WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1, "Times": 0, "Win": 0, "Lose": 0, "Profit": 0})
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == uid):
                    found_indices.append(i)
        try:
            i_value = found_indices[0]
        except IndexError:
            await ctx.send("The bot encountered an unexpected error. (Error ID: 142)")
            return 0

        try:
            if(str(params[0]).lower() not in ["calc", "table"]):
                await ctx.send("Invalid setting!")
                return 0
            if(str(params[0]).lower() == "calc"):
                try:
                    if(str(params[1]).lower() == "on"):
                        profile_data[i_value]["Calc"] = True
                    elif(str(params[1]).lower() == "off"):
                        profile_data[i_value]["Calc"] = False
                    else:
                        await ctx.send("Second parameter should be either \"on\" or \"off\"")
                        return 0
                except IndexError:
                    await ctx.send("Please provide what you want the setting to be equal to when you run the command!")
                    return 0
            if(str(params[0]).lower() == "table"):
                try:
                    if(str(params[1]).lower() == "on"):
                        profile_data[i_value]["Table"] = True
                    elif(str(params[1]).lower() == "off"):
                        profile_data[i_value]["Table"] = False
                    else:
                        await ctx.send("Second parameter should be either \"on\" or \"off\"")
                        return 0
                except IndexError:
                    await ctx.send("Please provide what you want the setting to be equal to when you run the command!")
                    return 0
            with open('profiles.json', 'w') as json_file:
                json.dump(profile_data, json_file)
            await ctx.send("Setting saved successfully!")
        except IndexError:
            if(profile_data[i_value]["Calc"]):
                calc_value = f"🟢 Enabled"
            else:
                calc_value = f"🔴 Disabled"
            if(profile_data[i_value]["Table"]):
                table_value = f"🟢 Enabled"
            else:
                table_value = f"🔴 Disabled"

            embedVar = discord.Embed(title=f"{ctx.author.name}'s Regents Question Settings", description=f"Use the command syntax `{self.info[3]}settings <calc/table> <on/off>` to change these settings", timestamp=datetime.utcnow(), color=0xFF0000)
            embedVar.add_field(
                name="Questions that require the use of a calculator", value=calc_value, inline=False)
            embedVar.add_field(
                name="Questions that require the use of the reference table", value=table_value, inline=False)
            await ctx.send(embed=embedVar)

    @commands.command(name='world', help="dispenses a Random AP World practice  question", aliases=['apworld', 'history'])
    async def world(self, ctx):
        found = 0
        with open('profiles.json') as f:
            profile_data = json.load(f)
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == ctx.author.id):
                found = 1
        if(found == 0):
            profile_data.append({"Name": ctx.author.name, "Tag": str(ctx.author), "Nick": ctx.author.display_name, "ID": ctx.author.id, "Avatar URL": str(
                ctx.author.avatar.url), "Correct": 0, "Total": 0, "Calc": True, "Table": True, "WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1, "Times": 0, "Win": 0, "Lose": 0, "Profit": 0})

        with open('questions/apworld.json') as f:
            questions = json.load(f)
        question_number = int(randint(0, len(questions)-1))

        embedVar = discord.Embed(
            title="Question #" + str(question_number + 1), timestamp=datetime.utcnow(), color=0xadd8e6)

        if(questions[question_number]['image'] != 0):
            embedVar.set_image(url=questions[question_number]['image'])

        embedVar.add_field(name=questions[question_number]['question'], value="a) " + str(questions[question_number]['choices'][0]) + "\nb) " + str(
            questions[question_number]['choices'][1]) + "\nc) " + str(questions[question_number]['choices'][2]) + "\nd) " + str(questions[question_number]['choices'][3]), inline=False)

        await ctx.reply(embed=embedVar)

        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and \
                msg.content.lower() in ["a", "b", "c", "d"]
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=90)
        except asyncio.TimeoutError:
            await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!")
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == ctx.author.id):
                    profile_data[i]['WorldTotal'] += 1
        if msg.content.lower() == questions[question_number]['answer']:
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == ctx.author.id):
                    profile_data[i]['WorldCorrect'] += 1
                    profile_data[i]['WorldTotal'] += 1
            await msg.reply("Correct!")
        else:
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == ctx.author.id):
                    profile_data[i]['WorldTotal'] += 1
            await msg.reply(f"Incorrect Answer. The correct answer was `{questions[question_number]['answer']}`")
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    @commands.command(name='apstats', help="dispenses a Random AP Stats practice  question")
    async def apstats(self, ctx):
        with open('questions/apstats.json') as f:
            questions = json.load(f)
        question_number = int(randint(0, len(questions)-1))

        embedVar = discord.Embed(
            title="Question #" + str(question_number + 1), timestamp=datetime.utcnow(), color=0xadd8e6)

        embedVar.set_image(url=questions[question_number]['image'])

        # embedVar.add_field(name=questions[question_number]['question'], value="a) " + str(questions[question_number]['choices'][0]) + "\nb) " + str(questions[question_number]['choices'][1]) + "\nc) " + str(questions[question_number]['choices'][2]) + "\nd) " + str(questions[question_number]['choices'][3] + "\ne) " + str(questions[question_number]['choices'][4])), inline=False)

        await ctx.reply(embed=embedVar)

        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and \
                msg.content.lower() in ["a", "b", "c", "d", "e"]
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=90)
        except asyncio.TimeoutError:
            await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!")
        if msg.content.lower() == questions[question_number]['answer']:
            await msg.reply("Correct!")
        else:
            await msg.reply(f"Incorrect Answer. The correct answer was `{questions[question_number]['answer']}`")

    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")


def setup(bot):
    bot.add_cog(Review(bot))
