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
    async def spam(self, ctx, *params):
        messages = ""
        for thing in params:
            messages += (str(thing) + " ")
        msg = f"{messages}"
        for i in range(5):
            await ctx.send(msg)

    @commands.command(name="ping", help="displays the latency to the bot.")
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency * 1000)}ms')

    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")


def setup(bot):
    bot.add_cog(Basic(bot))
