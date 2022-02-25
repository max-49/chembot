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
