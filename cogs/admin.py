import io
import os
import json
import discord
import chat_exporter
from config import get_bot
from discord.ext import commands
from discord.ext.commands import has_permissions, BadArgument, MissingRequiredArgument


'''
This class is a Cog which contains all commands to be listed under the Admin category.
'''
class Admin(commands.Cog):
    def __init__(self, bot):
        self.info = get_bot(os.getcwd().split('/')[-1])
        self.bot = bot

    '''
    The purge command allows everyone with permissions to manage messages to purge a number of recent messages.
    '''
    @commands.command(name='purge', help='deletes the most recent # of messages specified', usage='purge <# messages>')
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, num: int):
        await ctx.channel.purge(limit=num+1)
        await ctx.send(f'{num} messages cleared by {ctx.author.mention}')

    '''
    The purgeuser command is similar to the purge command, but deletes the most recent number of messages from a specific user.
    '''
    @commands.command(name='purgeuser', help='deletes the most recent # of messages specified by a certain user', usage='purgeuser <member> <# messages>')
    @has_permissions(manage_messages=True)
    async def purgeuser(self, ctx, member: discord.Member, num: int):
        if (num > 50):
            return await ctx.send("You can't purge more than 50 messages with this command!")
        history = [message async for message in ctx.channel.history(limit=100, oldest_first=False)]
        num_deleted = 0
        for message in history:
            if num_deleted == num:
                break
            elif message.author.id == member.id:
                await message.delete()
                num_deleted += 1
        else:
            await ctx.send("Number provided was more than this user's sent messages in this channel!")
        await ctx.send(f'{num_deleted} messages by {member} cleared by {ctx.author.mention}')

    '''
    This command just sends a large blank message to "clear" the screen of users
    '''
    @commands.command(name='clear', help="clears screen (admin only)", usage='clear')
    @has_permissions(administrator=True)
    async def clear(self, ctx):
        await ctx.send("_ _\n"*40)

    '''
    This command can be used to ban a user from the server with an optional reason to be included in the server audit log.
    '''
    @commands.command(name='ban', help="bans user", usage='ban <user> [reason]')
    @has_permissions(administrator=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        await user.ban(reason=reason, delete_message_days=0)
        await ctx.send(f"Banned {user.mention}")

    '''
    This command can be used to kick a user from the server with an optional reason to be included in the server audit log.
    '''
    @commands.command(name='kick', help="kicks user", usage='kick <user> [reason]')
    @has_permissions(administrator=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await user.kick(reason=reason)
        await ctx.send(f"Kicked {user.mention}")

    '''
    This command uses the chat_exporter library to create a transcript of a server channel as an HTML file to be saved for later.
    '''
    @commands.is_owner()
    @commands.command(name='save', help="saves an archive of the chat!", usage='save')
    async def save(self, ctx):
        await ctx.send("Saving...")
        transcript = await chat_exporter.export(ctx.channel, None, "EST")
        if transcript is None:
            await ctx.reply("Save resulted in no transcript being created! Please try again.")
            return
        transcript_file = discord.File(io.BytesIO(
            transcript.encode()), filename=f"archive-{ctx.channel.name}.html")
        await ctx.reply(file=transcript_file)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument) or isinstance(error, BadArgument):
            await ctx.reply(f"Incorrect syntax! Command usage: {self.info[3]}{ctx.command.usage}")
        else:
            await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")


async def setup(bot):
    await bot.add_cog(Admin(bot))
