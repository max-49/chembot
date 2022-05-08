import os
import discord
from discord import ui
from discord.ext import commands
from config import get_bot
from discord.ext.commands import BadArgument, MissingRequiredArgument


class Questionnaire(ui.Modal, title='Questionnaire Response'):
    name = ui.TextInput(label='Name')
    answer = ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)

class Butto(ui.View):
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label='A', style=discord.ButtonStyle.grey)
    async def a(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(Questionnaire())

class Test(commands.Cog):
    def __init__(self, bot):
        self.info = get_bot(os.getcwd().split('/')[-1])
        self.bot = bot

    @commands.command(name='test', help='purgury', usage="test")
    async def bubto(self, ctx):
        game = Butto()
        await ctx.send(view=game)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument) or isinstance(error, BadArgument):
            await ctx.reply(f"Incorrect syntax! Command usage: {self.info[3]}{ctx.command.usage}")
        else:
            await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")



def setup(bot):
    bot.add_cog(Test(bot))
