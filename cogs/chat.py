import discord
from discord.ext import commands

class ChatBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addchannel', help='add channel to chatbot')
    async def chat(self, ctx, channel: discord.TextChannel):
        await ctx.send(f"{message}")

    @commands.command(name='deletechannel', help='delete a channel from chatbot')
    async def deletechannel()

def setup(bot):
    bot.add_cog(ChatBot(bot))