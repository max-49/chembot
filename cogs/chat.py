import discord
from discord.ext import commands

class ChatBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addchannel', help='add channel to chatbot')
    async def chat(self, ctx, channel: discord.TextChannel):
        await ctx.send(f"{message}")

def setup(bot):
    bot.add_cog(ChatBot(bot))