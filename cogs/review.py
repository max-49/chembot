import os
import json
import discord
import asyncio
from random import randint
from utils import get_emoji
from datetime import datetime
from discord.ext import commands


class Review(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='profile', help="displays your profile")
    async def profile(self, ctx, profile="none"):
        if profile == "none":
            param = ""
        else:
            param = profile
        print(f"{ctx.author.name}: {'s!profile'} " + str(param))
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
        found_indices = []
        for i in range(len(profile_data)):
            user_mention = f"<@!{profile_data[i]['ID']}>"
            if(profile_data[i]['ID'] == uid or profile_data[i]['Name'] == uid or profile_data[i]['Nick'] == uid or profile_data[i]['Tag'] == uid or user_mention == uid):
                embedVar = discord.Embed(
                    title=f"{profile_data[i]['Name']}'s profile",  timestamp=datetime.utcnow(), color=0x00ff00)
                try:
                    percent_correct = (
                        profile_data[i]['Correct']/profile_data[i]['Total']) * 100
                except ZeroDivisionError:
                    percent_correct = 0
                try:
                    percent_world_correct = (
                        profile_data[i]['WorldCorrect']/profile_data[i]['WorldTotal']) * 100
                except ZeroDivisionError:
                    percent_world_correct = 0
                embedVar.add_field(name="Chemistry Regents Review Stats",
                                   value=f"{str(profile_data[i]['Correct'])}/{str(profile_data[i]['Total'])} ({str(round(percent_correct, 2))}%)", inline=False)
                embedVar.add_field(name="AP World Review Stats",
                                   value=f"{str(profile_data[i]['WorldCorrect'])}/{str(profile_data[i]['WorldTotal'])} ({str(round(percent_world_correct, 2))}%)", inline=False)
                embedVar.add_field(
                    name="Balance", value=f"{profile_data[i]['Balance']} schlucks", inline=False)
                embedVar.set_thumbnail(url=profile_data[i]['Avatar URL'])
                await ctx.send(embed=embedVar)
                found = 1
                found_indices.append(i)
        if(found == 0):
            isSameUser = 0
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == ctx.author.id):
                    await ctx.send("Looks like this user does not have a profile. Ask them to create one with `s!profile`!")
                    isSameUser = 1
                    break
            if(isSameUser == 0):
                profile_data.append({"Name": ctx.author.name, "Tag": str(ctx.author), "Nick": ctx.author.display_name, "ID": ctx.author.id, "Avatar URL": str(
                    ctx.author.avatar_url), "Correct": 0, "Total": 0, "Calc": "True", "Table": "True", "WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1})
                embedVar = discord.Embed(
                    title=f"{ctx.author.name}'s profile",  timestamp=datetime.utcnow(), color=0x00ff00)
                try:
                    percent_correct = (
                        profile_data[i]['Correct']/profile_data[i]['Total']) * 100
                except ZeroDivisionError:
                    percent_correct = 0
                embedVar.add_field(name="Chemistry Regents Review Stats",
                                   value=f"{str(profile_data[i]['Correct'])}/{str(profile_data[i]['Total'])} ({str(round(percent_correct, 2))}%)", inline=False)
                embedVar.add_field(name="AP World Review Stats",
                                   value=f"{str(profile_data[i]['WorldCorrect'])}/{str(profile_data[i]['WorldTotal'])} ({str(round(percent_world_correct, 2))}%)", inline=False)
                embedVar.set_thumbnail(url=profile_data[i]['Avatar URL'])
                await ctx.send(embed=embedVar)
        try:
            print(found_indices[1])
            profile_data.pop(found_indices[1])
        except IndexError:
            var = 1
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    @commands.command(name='regents', help="dispenses a Random regents question (syntax: s!regents (<atom>, <periodic>, <matter>, <solubility>")
    async def regents(self, ctx, *params):
        found = 0
        with open('profiles.json') as f:
            profile_data = json.load(f)
        found_indices = []
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == ctx.author.id):
                found = 1
                found_indices.append(i)
        if(found == 0):
            profile_data.append({"Name": ctx.author.name, "Tag": str(ctx.author), "Nick": ctx.author.display_name, "ID": ctx.author.id, "Avatar URL": str(
                ctx.author.avatar_url), "Correct": 0, "Total": 0, "Calc": "True", "Table": "True", "WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1})
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == ctx.author.id):
                    found = 1
                    found_indices.append(i)
        i_value = found_indices[0]
        try:
            category_choice = params[0]
            if(category_choice.lower() == "matter"):
                category = "Matter"
                with open('questions/matter.json') as f:
                    questions = json.load(f)
                if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
                    question_number = int(randint(0, len(questions)-1))
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        elif questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
            elif(category_choice.lower() == "atom"):
                category = "Atomic Structure"
                with open('questions/atom.json') as f:
                    questions = json.load(f)
                if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
                    question_number = int(randint(0, len(questions)-1))
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        elif questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
            elif(category_choice.lower() == "periodic"):
                category = "Periodic Table"
                with open('questions/periodic.json') as f:
                    questions = json.load(f)
                if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
                    question_number = int(randint(0, len(questions)-1))
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        elif questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
            elif(category_choice.lower() == "solubility"):
                category = "Solubility"
                with open('questions/solubility.json') as f:
                    questions = json.load(f)
                if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
                    question_number = int(randint(0, len(questions)-1))
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        elif questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
            elif(category_choice.lower() == "kinetics"):
                category = "Kinetics"
                with open('questions/kinetics.json') as f:
                    questions = json.load(f)
                if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
                    question_number = int(randint(0, len(questions)-1))
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        elif questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
            else:
                await ctx.send("Invalid Category. Choosing random category.")
                category_number = int(randint(0, 4))
                if(category_number == 0):
                    category = "Matter"
                    with open('questions/matter.json') as f:
                        questions = json.load(f)
                    if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
                        question_number = int(randint(0, len(questions)-1))
                    elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
                        while True:
                            question_number = int(randint(0, len(questions)-1))
                            if questions[question_number]["Calc"] == "True":
                                questions.pop(i)
                                continue
                            elif questions[question_number]["Table"] == "True":
                                questions.pop(i)
                                continue
                            else:
                                break
                    elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
                        while True:
                            question_number = int(randint(0, len(questions)-1))
                            if questions[question_number]["Table"] == "True":
                                questions.pop(i)
                                continue
                            else:
                                break
                    elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
                        while True:
                            question_number = int(randint(0, len(questions)-1))
                            if questions[question_number]["Calc"] == "True":
                                questions.pop(i)
                                continue
                            else:
                                break
                elif(category_number == 2):
                    category = "Periodic Table"
                    with open('questions/periodic.json') as f:
                        questions = json.load(f)
                    if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
                        question_number = int(randint(0, len(questions)-1))
                    elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
                        while True:
                            question_number = int(randint(0, len(questions)-1))
                            if questions[question_number]["Calc"] == "True":
                                questions.pop(i)
                                continue
                            elif questions[question_number]["Table"] == "True":
                                questions.pop(i)
                                continue
                            else:
                                break
                    elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
                        while True:
                            question_number = int(randint(0, len(questions)-1))
                            if questions[question_number]["Table"] == "True":
                                questions.pop(i)
                                continue
                            else:
                                break
                    elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
                        while True:
                            question_number = int(randint(0, len(questions)-1))
                            if questions[question_number]["Calc"] == "True":
                                questions.pop(i)
                                continue
                            else:
                                break
                elif(category_number == 3):
                    category = "Solubility"
                    with open('questions/solubility.json') as f:
                        questions = json.load(f)
                    if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
                        question_number = int(randint(0, len(questions)-1))
                    elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
                        while True:
                            question_number = int(randint(0, len(questions)-1))
                            if questions[question_number]["Calc"] == "True":
                                questions.pop(i)
                                continue
                            elif questions[question_number]["Table"] == "True":
                                questions.pop(i)
                                continue
                            else:
                                break
                    elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
                        while True:
                            question_number = int(randint(0, len(questions)-1))
                            if questions[question_number]["Table"] == "True":
                                questions.pop(i)
                                continue
                            else:
                                break
                    elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
                        while True:
                            question_number = int(randint(0, len(questions)-1))
                            if questions[question_number]["Calc"] == "True":
                                questions.pop(i)
                                continue
                            else:
                                break
                elif(category_number == 4):
                    category = "Kinetics"
                    with open('questions/kinetics.json') as f:
                        questions = json.load(f)
                    if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
                        question_number = int(randint(0, len(questions)-1))
                    elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
                        while True:
                            question_number = int(randint(0, len(questions)-1))
                            if questions[question_number]["Calc"] == "True":
                                questions.pop(i)
                                continue
                            elif questions[question_number]["Table"] == "True":
                                questions.pop(i)
                                continue
                            else:
                                break
                    elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
                        while True:
                            question_number = int(randint(0, len(questions)-1))
                            if questions[question_number]["Table"] == "True":
                                questions.pop(i)
                                continue
                            else:
                                break
                    elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
                        while True:
                            question_number = int(randint(0, len(questions)-1))
                            if questions[question_number]["Calc"] == "True":
                                questions.pop(i)
                                continue
                            else:
                                break

        except IndexError:
            category_number = int(randint(0, 4))
            if(category_number == 0):
                category = "Matter"
                with open('questions/matter.json') as f:
                    questions = json.load(f)
                if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
                    question_number = int(randint(0, len(questions)-1))
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        elif questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
            elif(category_number == 1):
                category = "Atomic Structure"
                with open('questions/atom.json') as f:
                    questions = json.load(f)
                if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
                    question_number = int(randint(0, len(questions)-1))
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        elif questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
            elif(category_number == 2):
                category = "Periodic Table"
                with open('questions/periodic.json') as f:
                    questions = json.load(f)
                if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
                    question_number = int(randint(0, len(questions)-1))
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        elif questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
            elif(category_number == 3):
                category = "Solubility"
                with open('questions/solubility.json') as f:
                    questions = json.load(f)
                if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
                    question_number = int(randint(0, len(questions)-1))
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        elif questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
            elif(category_number == 4):
                category = "Kinetics"
                with open('questions/kinetics.json') as f:
                    questions = json.load(f)
                if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
                    question_number = int(randint(0, len(questions)-1))
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
                            questions.pop(i)
                            continue
                        elif questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Table"] == "True":
                            questions.pop(i)
                            continue
                        else:
                            break
                elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
                    while True:
                        question_number = int(randint(0, len(questions)-1))
                        if questions[question_number]["Calc"] == "True":
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

        if(questions[question_number]['Calc'] == "True"):
            if(questions[question_number]['Table'] == "True"):
                embedVar.add_field(
                    name="Tools required", value="Calculator and Reference Table", inline=False)
            elif(questions[question_number]['Table'] == "False"):
                embedVar.add_field(name="Tools required",
                                   value="Calculator", inline=False)
        elif(questions[question_number]['Table'] == "True"):
            if(questions[question_number]['Calc'] == "True"):
                embedVar.add_field(
                    name="Tools required", value="Calculator and Reference Table", inline=False)
            elif(questions[question_number]['Calc'] == "False"):
                embedVar.add_field(name="Tools required",
                                   value="Reference Table", inline=False)

        embedVar.add_field(name="Category", value="`" +
                           str(category)+"`", inline=False)

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
                    profile_data[i]['Total'] += 1
        if msg.content.lower() == questions[question_number]['answer']:
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == ctx.author.id):
                    profile_data[i]['Correct'] += 1
                    profile_data[i]['Total'] += 1
            await msg.reply("Correct!")
        else:
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == ctx.author.id):
                    profile_data[i]['Total'] += 1
            await msg.reply(f"Incorrect Answer. The correct answer was `{questions[question_number]['answer']}`.\nYou should probably review the `{category}` unit.")
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    @commands.command(name='review', help="dispenses a review question (kinetics)")
    async def review(self, ctx, *params):
        param = ""
        for thing in params:
            param += str(thing) + " "
        print(f"{ctx.author.name}: {'s!review'} " + str(param))
        with open('questions/kinetics.json') as f:
            questions = json.load(f)
        question_number = int(randint(0, len(questions)-1))

        embedVar = discord.Embed(
            title="Question #" + str(question_number + 1), timestamp=datetime.utcnow(), color=0xD3D3D3)

        if(questions[question_number]['image'] != 0):
            embedVar.set_image(url=questions[question_number]['image'])

        embedVar.add_field(name=questions[question_number]['question'], value="a) " + str(questions[question_number]['choices'][0]) + "\nb) " + str(
            questions[question_number]['choices'][1]) + "\nc) " + str(questions[question_number]['choices'][2]) + "\nd) " + str(questions[question_number]['choices'][3]), inline=False)

        embedVar.add_field(name="Category", value="`Kinetics`", inline=False)

        await ctx.reply(embed=embedVar)

        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and \
                msg.content.lower() in ["a", "b", "c", "d"]

        attempts = 1
        while True:
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=90)
            except asyncio.TimeoutError:
                await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!")
                return 0
            if msg.content.lower() == questions[question_number]['answer']:
                await msg.reply("Correct!")
                return 0
            else:
                if(attempts != 0):
                    await msg.reply(f"Incorrect answer. You have {attempts} attempts left")
                    attempts -= 1
                    continue
                else:
                    await msg.reply(f"Incorrect Answer. The correct answer was `{questions[question_number]['answer']}`.")
                    return 0

    @commands.command(name='leaderboard', help="Displays the global leaderboards", aliases=['lb', 'leader'])
    async def lb(self, ctx, *params):
        with open('profiles.json') as f:
            profile_data = json.load(f)
        percentages = {}
        try:
            if(str(params[0]).lower() in ['world', 'chem', 'apworld', 'chemistry', 'bal', 'money', 'rich', 'schlucks']):
                if(str(params[0]).lower() == 'world' or str(params[0]).lower() == 'apworld'):
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
                    embedVar.add_field(name="Placements",
                                       value=msg, inline=False)
                    await ctx.send(embed=embedVar)
                elif(str(params[0]).lower() == 'bal' or str(params[0]).lower() == 'money' or str(params[0]).lower() == 'rich' or str(params[0]).lower() == 'schlucks'):
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
                    embedVar.add_field(name="Placements",
                                       value=msg, inline=False)
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
                    embedVar.add_field(name="Placements",
                                       value=msg, inline=False)
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
        except IndexError:
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
                ctx.author.avatar_url), "Correct": 0, "Total": 0, "Calc": "True", "Table": "True", "WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1})
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
                        profile_data[i_value]["Calc"] = "True"
                    elif(str(params[1]).lower() == "off"):
                        profile_data[i_value]["Calc"] = "False"
                    else:
                        await ctx.send("Second parameter should be either \"on\" or \"off\"")
                        return 0
                except IndexError:
                    await ctx.send("Please provide what you want the setting to be equal to when you run the command!")
                    return 0
            if(str(params[0]).lower() == "table"):
                try:
                    if(str(params[1]).lower() == "on"):
                        profile_data[i_value]["Table"] = "True"
                    elif(str(params[1]).lower() == "off"):
                        profile_data[i_value]["Table"] = "False"
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
            if(profile_data[i_value]["Calc"] == "True"):
                calc_value = f"{get_emoji('green_circle')} Enabled"
            else:
                calc_value = f"{get_emoji('red_circle')} Disabled"
            if(profile_data[i_value]["Table"] == "True"):
                table_value = f"{get_emoji('green_circle')} Enabled"
            else:
                table_value = f"{get_emoji('red_circle')} Disabled"

            embedVar = discord.Embed(title=f"{ctx.author.name}'s Regents Question Settings",
                                     description="Use the command syntax `s!settings <calc/table> <on/off>` to change these settings", timestamp=datetime.utcnow(), color=0xFF0000)
            embedVar.add_field(
                name="Questions that require the use of a calculator", value=calc_value, inline=False)
            embedVar.add_field(
                name="Questions that require the use of the reference table", value=table_value, inline=False)
            await ctx.send(embed=embedVar)

    @commands.command(name='world', help="dispenses a Random AP World practice  question", aliases=['apworld', 'history'])
    async def world(self, ctx, *params):
            found = 0
            with open('profiles.json') as f:
                profile_data = json.load(f)
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == ctx.author.id):
                    found = 1
            if(found == 0):
                profile_data.append({"Name": ctx.author.name, "Tag": str(ctx.author), "Nick": ctx.author.display_name, "ID": ctx.author.id, "Avatar URL": str(
                    ctx.author.avatar_url), "Correct": 0, "Total": 0, "Calc": "True", "Table": "True", "WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1})

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
    async def apstats(self, ctx, *params):
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
