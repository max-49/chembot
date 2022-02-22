import os
import json
import aiohttp
import discord
from random import randint
from datetime import datetime
from discord.ext import commands

class Website(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label='Visit Max49\'s Website', url="https://www.max49.cf"))

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='amongus', help='yo')
    async def smthg(self, ctx):
        await ctx.invoke(self.bot.get_command('gif'), search_term="among us")

    @commands.command(name='pfp', help="Displays a profile picture", pass_context=True)
    async def pfp(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(f'{ctx.author.avatar.url}')
        else:
            await ctx.send(f'{member.avatar.url}')

    @commands.command(name='info', help="Displays information about this bot")
    async def info(self, ctx):
        embed = discord.Embed(
            title="Bot Info", timestamp=datetime.utcnow(), color=0x00ff00)
        embed.add_field(
            name="Creator", value="Made by Max49#9833", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/427832149173862400/1767e28d50d41fab9872c7137020df9c.webp?size=1024")
        await ctx.send(embed=embed, view=Website())

    @commands.command(name='gif', help="sends a random gif", aliases=['g'])
    async def gif(self, ctx, *, search_term: str):
        api_key = os.getenv('GIPHY_KEY')

        async def search_gifs(query):
            try:
                session = aiohttp.ClientSession()
                response = await session.get(f"https://g.tenor.com/v1/search?q={search_term}&key={api_key}&limit=50")
                data = json.loads(await response.text())
                gif_choice = randint(0, 40)
                gif_url = data['results'][gif_choice]['media'][0]['gif']['url']
                await session.close()
                return gif_url
            except IndexError:
                await session.close()
                return "No gifs found for that query!"
        gif = await search_gifs(search_term)
        await ctx.send(gif)

    @commands.command(name='spam', help="spams text")
    async def spam(self, ctx, *, string: str):
        if(ctx.guild.id == 732308165265326080):
            return await ctx.send("no spam in ictf bc it makes wick sad")
        for i in range(5):
            await ctx.send(string, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))

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
            embed = discord.Embed(
                title=f"{self.bot.user.name} Help", color=0x00ff00)
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
            embed = discord.Embed(
                title=f"{self.bot.user.name} Help", color=0x00ff00)
            try:
                for key, value in help_list[number].items():
                    field = ""
                    for thing in value:
                        field += f"{thing}\n"
                    embed.add_field(name=key, value=field, inline=False)
                    embed.set_footer(text=f"{number + 1}/{len(help_list)}")
            except UnboundLocalError:
                number = 0
                embed = discord.Embed(
                    title=f"{self.bot.user.name} Help", color=0x00ff00)
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
                embed = discord.Embed(
                    title=f"{self.bot.user.name} Help", color=0x00ff00)
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
                embed = discord.Embed(
                    title=f"{self.bot.user.name} Help", color=0x00ff00)
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
