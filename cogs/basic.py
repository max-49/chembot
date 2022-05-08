import os
import json
import aiohttp
import discord
from config import get_bot
from random import randint
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import BadArgument, MissingRequiredArgument

class Website(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label='Visit Max49\'s Website', url="https://www.max49.cf"))

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.info = get_bot(os.getcwd().split('/')[-1])

    @commands.command(name='pfp', help="Displays a profile picture", usage="pfp [member]")
    async def pfp(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(f'{ctx.author.avatar.url}')
        else:
            await ctx.send(f'{member.avatar.url}')

    @commands.command(name='info', help="Displays information about this bot", usage="info")
    async def info(self, ctx):
        embed = discord.Embed(
            title="Bot Info", timestamp=datetime.utcnow(), color=0x00ff00)
        embed.add_field(
            name="Creator", value="Made by Max49#9833", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/427832149173862400/1767e28d50d41fab9872c7137020df9c.webp?size=1024")
        await ctx.send(embed=embed, view=Website())

    @commands.command(name='gif', help="sends a random gif", aliases=['g'], usage="gif <search query>")
    async def gif(self, ctx, *, search_term: str):
        api_key = os.getenv('GIPHY_KEY')

        async def search_gifs(query):
            try:
                session = aiohttp.ClientSession()
                response = await session.get(f"https://g.tenor.com/v1/search?q={query}&key={api_key}&limit=50")
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

    @commands.command(name='spam', help="spams text", usage="spam <message>")
    async def spam(self, ctx, *, string: str):
        if(ctx.guild.id == 732308165265326080):
            return await ctx.send("no spam in ictf bc it makes wick sad")
        for _ in range(5):
            await ctx.send(string, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))

    @commands.command(name="ping", help="displays the latency to the bot.", usage="ping")
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency * 1000)}ms')

    @commands.command(name='help', help='displays this message!', usage="help [cog, command]")
    async def help(self, ctx, *, select_cog=None):
        help_list = []

        if select_cog in self.bot.all_commands:
            command = self.bot.all_commands[select_cog]
            embed = discord.Embed(title=f"{self.info[3]}{command.name}", color=0x00ff00)
            embed.add_field(name="Usage", value=f"{self.info[3]}{command.usage}", inline=False)
            if command.aliases is not None:
                embed.add_field(name="Aliases", value=f"{', '.join(command.aliases)}", inline=False)
            return await ctx.send(embed=embed)

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
                for key in commands[i]:
                    if str(key) == str(embed.fields[0].name):
                        number = i
            if str(reaction.emoji) == "⬅️":
                new_embed = get_next_embed(commands, number, 0)
                if new_embed is not None:
                    await reaction.message.edit(embed=new_embed)
            if str(reaction.emoji) == "➡️":
                new_embed = get_next_embed(commands, number, 1)
                if new_embed is not None:
                    await reaction.message.edit(embed=new_embed)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument) or isinstance(error, BadArgument):
            await ctx.reply(f"Incorrect syntax! Command usage: {self.info[3]}{ctx.command.usage}")
        else:
            await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")



def setup(bot):
    bot.add_cog(Basic(bot))
