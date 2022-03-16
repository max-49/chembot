import io
import os
import json
import string
import discord
import chat_exporter
from discord.ext import commands
from discord.ext.commands import has_permissions


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='purge', help='purgury')
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, num: int):
        await ctx.channel.purge(limit=num+1)
        await ctx.send(f'{num} messages cleared by {ctx.author.mention}')

    @commands.command(name='purgeuser', help='purgury in channel')
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

    @commands.command(name='clear', help="clears screen (admin only)")
    @has_permissions(administrator=True)
    async def clear(self, ctx):
        await ctx.send("_ _\n"*40)

    @commands.command(name='ban', help="ban", hidden=True)
    @has_permissions(administrator=True)
    async def ban(self, ctx, user: discord.Member=None, *, reason=None):
        if user is None:
            await ctx.send("Please specify a user to ban.")
            return
        await user.ban(reason=reason)
        await ctx.send(f"Banned {user.mention}")

    @commands.command(name='kick', help="kick", hidden=True)
    @has_permissions(administrator=True)
    async def kick(self, ctx, user: discord.Member=None, *, reason=None):
        if user is None:
            await ctx.send("Please specify a user to kick.")
            return
        await user.kick(reason=reason)
        await ctx.send(f"Kicked {user.mention}")

    @commands.command(name='save', help="saves an archive of the chat!")
    async def save(self, ctx, *params):
        with open('allowed_ids.json') as j:
            allowed_ids = json.load(j)
        try:
            if(ctx.author.id == 427832149173862400 or ctx.author.guild_permissions.administrator):
                if(params[0] == "allowId"):
                    if int(params[1]) not in allowed_ids:
                        allowed_ids.append(int(params[1]))
                        await ctx.reply("Successfully added ID to allowed IDs!")
                    else:
                        await ctx.reply("This ID is already allowed to archive chats!")
                elif(params[0] == "denyId"):
                    if int(params[1]) in allowed_ids:
                        allowed_ids.remove(int(params[1]))
                        await ctx.reply("Successfully denied user from archiving chats!")
                    else:
                        await ctx.reply("This ID already isn't allowed to archive chats!")
        except IndexError:
            if(ctx.author.id == 427832149173862400 or ctx.author.guild_permissions.administrator or int(ctx.author.id) in allowed_ids):
                await ctx.send("Saving...")
                transcript = await chat_exporter.export(ctx.channel, None, "EST")
                if transcript is None:
                    await ctx.reply("Save resulted in no transcript being created! Please try again.")
                    return
                transcript_file = discord.File(io.BytesIO(
                    transcript.encode()), filename=f"archive-{ctx.channel.name}.html")
                await ctx.reply(file=transcript_file)
        with open('allowed_ids.json', 'w') as j:
            json.dump(allowed_ids, j)

    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")


def setup(bot):
    bot.add_cog(Admin(bot))
