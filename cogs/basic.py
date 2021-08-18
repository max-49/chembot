import os
import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord_components import Button, ButtonStyle
from datetime import datetime
import os
import json
import aiohttp
from random import randint

converter = MemberConverter()


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pfp', help="Displays a profile picture (syntax: s!pfp <mention>)")
    async def pfp(self, ctx, mention="None"):
        if(mention == "None"):
            await ctx.send(f'{ctx.author.avatar_url}')
        else:
            try:
                member = await converter.convert(ctx, mention)
            except discord.ext.commands.errors.MemberNotFound as err:
                await ctx.send(f'{err}')
                return 0
            await ctx.send(f'{member.avatar_url}')

    @commands.command(name='info', help="Displays information about this bot")
    async def info(self, ctx):
        embed = discord.Embed(
            title="Bot Info", timestamp=datetime.utcnow(), color=0x00ff00)
        embed.add_field(
            name="Creator", value="Made by Max49#9833", inline=False)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/427832149173862400/1767e28d50d41fab9872c7137020df9c.webp?size=1024")
        await ctx.send(embed=embed)
        await ctx.channel.send("Click the button below to visit my website!", components=[Button(style=ButtonStyle.URL, label="Visit Max's Website!", url="https://www.max49.cf/"), ])

    @commands.command(name='gif', help="sends a random gif (syntax: s!gif <search>")
    async def gif(self, ctx, *search):
        search_term = ""
        for thing in search:
            search_term += (str(thing) + " ")
        api_key = os.getenv('GIPHY_KEY')

        async def search_gifs(query):
          try:
            session = aiohttp.ClientSession()
            response = await session.get(f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={query}&limit=50&offset=0")
            data = json.loads(await response.text())
            gif_choice = randint(0, 30)
            gif_url = data['data'][gif_choice]['images']['original']['url']
            await session.close()
            return gif_url
          except IndexError:
            await session.close()
            return "No gifs found for that query!"
        gif = await search_gifs(search_term)
        await ctx.send(gif)

    @commands.command(name='spam', help="spams text")
    async def spam(self, ctx, *, string: str):
        for i in range(5):
            await ctx.send(string)

    @commands.command(name="ping", help="displays the latency to the bot.")
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency * 1000)}ms')

    @commands.command(name='help', help='displays this message!')
    async def help(self, ctx, *, select_cog=None):
        help_list = []
        num = 0

        for cog in self.bot.cogs:
            help_dict = {}
            cog_coms = []
            walk_cog = self.bot.get_cog(cog)
            commands = walk_cog.get_commands()
            for command in commands:
                if not command.hidden:
                    cog_coms.append(f'{command.name} - {command.help}')
            help_dict[cog] = cog_coms
            help_list.append(help_dict)
            num += 1

        if select_cog is None:
            number = 0
            embed = discord.Embed(title="ChemBot Help", color=0x00ff00)
            for key, value in help_list[number].items():
                field = ""
                for thing in value:
                    field += f"{thing}\n" 
                embed.add_field(name=key, value=field, inline=False)
                embed.set_footer(text=f"{number + 1}/{len(help_list)}")
        else:
            for i in range(len(help_list)):
                for key, value in help_list[i].items():
                        if str(key.lower()) == str(select_cog.lower()):
                            number = i
            embed = discord.Embed(title="ChemBot Help", color=0x00ff00)
            for key, value in help_list[number].items():
                field = ""
                for thing in value:
                    field += f"{thing}\n" 
                embed.add_field(name=key, value=field, inline=False)
                embed.set_footer(text=f"{number + 1}/{len(help_list)}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')

        with open('commands.json', 'w') as j:
            json.dump(help_list, j)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        def get_next_embed(embeds, number, react):
            if number == 0 and react == 0 or number == len(embeds) - 1 and react == 1:
                return None
            if react == 0:
                number -= 1
                new_embed_data = embeds[number]
                embed = discord.Embed(title="ChemBot Help", color=0x00ff00)
                for key, value in new_embed_data.items():
                    field = ""
                    for thing in value:
                        field += f"{thing}\n" 
                    embed.add_field(name=key, value=field, inline=False)
                    embed.set_footer(text=f"{number + 1}/{len(embeds)}")
                return embed
            elif react == 1:
                number += 1
                new_embed_data = embeds[number]
                embed = discord.Embed(title="ChemBot Help", color=0x00ff00)
                for key, value in new_embed_data.items():
                    field = ""
                    for thing in value:
                        field += f"{thing}\n" 
                    embed.add_field(name=key, value=field, inline=False)
                    embed.set_footer(text=f"{number + 1}/{len(embeds)}")
                return embed
                
        with open('commands.json') as j:
            commands = json.load(j)
        if reaction.message.author.id == self.bot.user.id and user != self.bot.user:
            embed = reaction.message.embeds[0]
            for i in range(len(commands)):
                for key, value in commands[i].items():
                    for keyy in value:
                        if str(key) == str(embed.fields[0].name):
                            number = i
            if str(reaction.emoji) == "⬅️":
                newEmbed = get_next_embed(commands, number, 0)
                if newEmbed is not None:
                    await reaction.message.edit(embed=newEmbed)
            if str(reaction.emoji) == "➡️":
                newEmbed = get_next_embed(commands, number, 1)
                if newEmbed is not None:
                    await reaction.message.edit(embed=newEmbed)


    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")


def setup(bot):
    bot.add_cog(Basic(bot))
