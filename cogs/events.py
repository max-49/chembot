import os
import json
import time
import string
import discord
import datetime
from pytz import timezone
from datetime import timedelta
from discord.ext import commands, tasks

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.event_handler.start()

    def cog_unload(self):
        self.event_handler.cancel()

    @tasks.loop(seconds=60.0)
    async def event_handler(self):
        if(datetime.datetime.utcnow() == 0):
            with open('profiles.json') as j:
                profile_data = json.load(j)
            for i in range(len(profile_data)):
                profile_data[i]['didDaily'] = False
            with open('profiles.json', 'w') as j:
                json.dump(profile_data, j)
        
        with open('events.json') as j:
            events = json.load(j)
        events = sorted(events, key = lambda i: i['unix_time'])
        if(len(events) > 0):
            most_recent_event = events[0]
            if(((datetime.datetime.fromtimestamp(most_recent_event['unix_time']) - timedelta(hours=5)) < datetime.datetime.now(timezone('EST')).replace(tzinfo=None))):
                embed = discord.Embed(title="Event!", timestamp=datetime.datetime.utcnow(), color=0x00FF00)
                embed.add_field(name=f"{most_recent_event['creator_name']}'s event", value=most_recent_event['message'])
                try:
                    channel = self.bot.get_channel(int(most_recent_event['channel'][2:-1]))
                except:
                    channel = self.bot.get_channel(780586194257182760)
                user = ""
                if(most_recent_event['user_ping']):
                    user += f"<@{most_recent_event['creator_id']}>"
                await channel.send(f"{user}, {most_recent_event['others']}", embed=embed, allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=False))
                events.pop(0)
                with open('events.json', 'w') as w:
                    json.dump(events, w)

    @commands.command(name="addevent", help="addevent!")
    async def addevent(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and msg.content.lower()[0] in string.printable
        
        def check_yn(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and msg.content.lower() in ['y', 'n']
        
        date_mess = await ctx.send(f"{ctx.author.mention}, please enter the date of this event in the format MM/DD/YYYY (i.e. for the date of April 24th, 2023, enter 04/24/2023)")
        date = await self.bot.wait_for("message", check=check)
        await date_mess.delete()
        await date.delete()
        event_mess = await ctx.send(f"{ctx.author.mention}, please enter the time of this event IN MILITARY TIME in the format HH:MM (i.e. for the time of 10:30pm, enter 22:30)")
        event_time = await self.bot.wait_for("message", check=check)
        await event_mess.delete()
        await event_time.delete()
        message_mess = await ctx.send(f"{ctx.author.mention}, what is the event? (Please enter the message you want to be pinged with when this event happens)")
        message = await self.bot.wait_for("message", check=check)
        await message_mess.delete()
        await message.delete()
        channel_mess = await ctx.send(f"{ctx.author.mention}, what channel do you want this message to be sent in? Please mention it.")
        channel = await self.bot.wait_for("message", check=check)
        await channel_mess.delete()
        await channel.delete()
        user_mess = await ctx.send(f"{ctx.author.mention}, would you like to be pinged for this event (y/n)?")
        user_ping = await self.bot.wait_for("message", check=check_yn)
        await user_mess.delete()
        await user_ping.delete()
        other_mess = await ctx.send(f"{ctx.author.mention}, would you like another role/person to be pinged for this event (y/n)?")
        other_ping = await self.bot.wait_for("message", check=check_yn)
        await other_mess.delete()
        await other_ping.delete()
        other_message = ""
        if (other_ping.content == 'y'):
            others_mess = await ctx.send(f"{ctx.author.mention}, please enter all the role/user pings that should be pinged when this event occurs, separated by commas.")
            others = await self.bot.wait_for("message", check=check)
            await others_mess.delete()
            await date.delete()
            other_message = others.content
        date_split = date.content.split('/')
        time_split = event_time.content.split(':')
        if user_ping.content == 'y':
            user_ping = True
        else:
            user_ping = False
        try:
            datetime_date = (datetime.datetime(int(date_split[2]), int(date_split[0]), int(date_split[1]), int(time_split[0]), int(time_split[1]))) + timedelta(hours=5)
            datetime_unix = time.mktime(datetime_date.timetuple())
        except:
            return await ctx.send("Something went wrong! Please make sure your date and time followed the format!")
        if(((datetime.datetime.fromtimestamp(datetime_unix) - timedelta(hours=5)) < datetime.datetime.now(timezone('EST')).replace(tzinfo=None))):
            return await ctx.send("You can't make an event that would have happened in the past!")
        try:
            with open('events.json') as j:
                events = json.load(j)
        except json.decoder.JSONDecodeError:
            events = []
        events.append({"event_number": len(events) + 1, "unix_time": int(datetime_unix), "message": message.content, "channel": channel.content, "user_ping": user_ping, "others": other_message, "creator_name": ctx.author.name, "creator_id": ctx.author.id})
        await ctx.send("Your event has been successfully added!")       
        with open('events.json', 'w') as w:
            json.dump(events, w)

    @commands.command(name='listevents', help='list the events!')
    async def listevents(self, ctx):
        with open('events.json') as j:
            events = json.load(j)
        embed = discord.Embed(title='Upcoming events:', timestamp=datetime.datetime.utcnow(), color=0x0000FF)
        events = sorted(events, key = lambda i: i['unix_time'])
        if len(events) > 4:
            events = events[0:4]
        for event in events:
            time_diff = (datetime.datetime.fromtimestamp(event['unix_time']) - timedelta(hours=5)) - datetime.datetime.now(timezone('EST')).replace(tzinfo=None)
            if ((time_diff.seconds/3600) < 1):
                extra_message = f"{round(time_diff.seconds/60, 1)} minutes"
            else:
                extra_message = f"{round(time_diff.seconds/3600, 1)} hours"
            if(len(event['message']) > 20):
                event_message = f"{event['message'][0:20]}..."
            else:
                event_message = event['message']
            desc = f"*{event_message}*\nTime until event: {time_diff.days} days, {extra_message} from now"
            embed.add_field(name=f"{event['creator_name']}'s event", value=desc, inline=False)
        await ctx.send(embed=embed)

    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")

def setup(bot):
    bot.add_cog(Events(bot))