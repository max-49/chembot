import random
import discord
from discord.ext import commands
from datetime import datetime

class Spaces(discord.ui.View):
    def __init__(self, word: str):
        super().__init__()
        self.value = None
        self.word = word

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
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
        await interaction.message.edit(view=self)
        self.stop()

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def b(self, button: discord.ui.Button, interaction: discord.Interaction):
        if(self.correct == 'b'):
            await interaction.response.send_message('Correct!', ephemeral=True)         
            button.style = discord.ButtonStyle.green
            self.value = True
        else:
            await interaction.response.send_message(f'Incorrect! The correct answer was {self.correct}. You should probably review the {self.category} unit.', ephemeral=True)
            button.style = discord.ButtonStyle.red
            self.value = False
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        self.stop()

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def c(self, button: discord.ui.Button, interaction: discord.Interaction):
        if(self.correct == 'c'):
            await interaction.response.send_message('Correct!', ephemeral=True)     
            button.style = discord.ButtonStyle.green
            self.value = True       
        else:
            await interaction.response.send_message(f'Incorrect! The correct answer was {self.correct}. You should probably review the {self.category} unit.', ephemeral=True)
            button.style = discord.ButtonStyle.red
            self.value = False   
        for child in self.children:
            child.disabled = True        
        await interaction.message.edit(view=self)
        self.stop()
    
    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def d(self, button: discord.ui.Button, interaction: discord.Interaction):
        if(self.correct == 'd'):
            await interaction.response.send_message('Correct!', ephemeral=True)
            button.style = discord.ButtonStyle.green
            self.value = True           
        else:
            await interaction.response.send_message(f'Incorrect! The correct answer was {self.correct}. You should probably review the {self.category} unit.', ephemeral=True)
            button.style = discord.ButtonStyle.red
            self.value = False
        for child in self.children:
            child.disabled = True  
        await interaction.message.edit(view=self)
        self.stop()

    @discord.ui.button(label='\u200b', style=discord.ButtonStyle.grey)
    async def e(self, button: discord.ui.Button, interaction: discord.Interaction):
        if(self.correct == 'e'):
            await interaction.response.send_message('Correct!', ephemeral=True)
            button.style = discord.ButtonStyle.green
            self.value = True
        else:
            await interaction.response.send_message(f'Incorrect! The correct answer was {self.correct}. You should probably review the {self.category} unit.', ephemeral=True)   
            button.style = discord.ButtonStyle.red
            self.value = False  
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.author:
            return True
        else:
            await interaction.response.send_message('This button isn\'t for you!', ephemeral=True)
            return False

class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wordle", help="world")
    async def wordle(self, ctx):
        await ctx.send("im aliveaa")
        words = []

        with open('words.txt') as j:
            for line in j.readlines():
                words.append(line.strip())

        date = datetime.now().date()
        word = words[int(((date.year * date.day) / date.month) % len(word))]
        await ctx.send('before class declaration')
        game = Spaces(word)
        embed = discord.Embed(title="wordle")
        await ctx.send("right before sending view")
        await ctx.send(embed=embed, view=game)

    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")


def setup(bot):
    bot.add_cog(Wordle(bot))