#WaLLE
import asyncio
import urllib
import requests
import re
import random
import json
import base64
import binascii
import collections
import string
import sys
import os
import urllib.parse
from urllib.request import urlopen
import io
from dateutil.parser import parse
import time
import datetime
from datetime import timezone
from datetime import datetime
import discord
from discord.ext.commands import *
from discord.ext import commands
from colorthief import ColorThief
from help_info import *
from auth import *

import traceback
import logging as log

from trim import trim_nl
#from cogs.ctfmodel import TaskFailed
import discord
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
import youtube_dl

creator_id = [412077060207542284, 491610275993223170]

client = discord.Client()
bot = commands.Bot(command_prefix='!')
extensions = ['encoding_decoding', 'cipher', 'ctfs', 'utility', 'settings']
bot.remove_command('help')
blacklisted = []
cool_names = ['nullpxl', 'Test_Monkey', 'Yiggles', 'JohnHammond', 'voidUpdate',
        'Michel Ney', 'theKidOfArcrania', 'knapstack']

load_dotenv()
# # Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("discord_token")

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


@bot.command()
async def play(ctx,url):
    
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command()
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command()
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")
    


@bot.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command()
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.event
async def on_ready():
    print('Running!')
    for guild in bot.guilds:
        for channel in guild.text_channels :
            if str(channel) == "general" :
                await channel.send('Bot Activated..')
                await channel.send(file=discord.File('giphy.png'))
        print('Active in {}\n Member Count : {}'.format(guild.name,guild.member_count))

@bot.command(help = "Prints details of Author")
async def whats_author(ctx) :
    await ctx.send('Hello Akiekano')

@bot.command()
async def where_am_i(ctx):
    owner=str(ctx.guild.owner)
    region = str(ctx.guild.region)
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    desc=ctx.guild.description
    
    embed = discord.Embed(
        title=ctx.guild.name + " Server Information",
        description=desc,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)
    


@bot.event
async def on_member_join(member):
     for channel in member.guild.text_channels :
         if str(channel) == "general" :
             on_mobile=False
             if member.is_on_mobile() == True :
                 on_mobile = True
             await channel.send("Welcome to the Server {}!!\n On Mobile : {}".format(member.name,on_mobile))             
        
# TODO : Filter out swear words from messages

@bot.command()
async def tell_me_about_yourself(ctx):
    text = "My name is WallE!\n I was built by Kakarot2000. At present I have limited features(find out more by typing !help)\n :)"
    await ctx.send(text)

@bot.event
async def on_message(message) :
    # bot.process_commands(msg) is a couroutine that must be called here since we are overriding the on_message event
    await bot.process_commands(message) 
    if str(message.content).lower() == "hello":
        await message.channel.send('Hi!')
    
    if str(message.content).lower() in ['swear_word1','swear_word2']:
        await message.channel.purge(limit=1)

@bot.event
async def on_ready():
    print(('<' + bot.user.name) + ' Online>')
    print(discord.__version__)
    await bot.change_presence(activity=discord.Game(name='!help / !report "issue"'))

@bot.event
async def on_message(message):
    if 'who should I subscribe to?' in message.content:
        choice = random.randint(1, 2)
        
        if choice == 1:
            await message.channel.send('https://youtube.com/nullpxl')
        
        if choice == 2:
            await message.channel.send('https://www.youtube.com/user/RootOfTheNull')
    
    await bot.process_commands(message)

@bot.event
async def on_error(evt_type, ctx):
    if evt_type == 'on_message':
        await ctx.send('An error has occurred... :disappointed:')
    log.error(f'Ignoring exception at {evt_type}')
    log.error(traceback.format_exc())


@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, MissingPermissions):
        await ctx.send('You do not have permission to do that! ¯\_(ツ)_/¯')
    elif isinstance(err, BotMissingPermissions):
        await ctx.send(trim_nl(f''':cry: I can\'t do that. Please ask server ops
        to add all the permission for me!
        
        ```{str(err)}```'''))
    elif isinstance(err, DisabledCommand):
        await ctx.send(':skull: Command has been disabled!')
    elif isinstance(err, CommandNotFound):
        await ctx.send('Invalid command passed. Use !help.')
    elif isinstance(err, TaskFailed):
        await ctx.send(f':bangbang: {str(err)}')
    elif isinstance(err, NoPrivateMessage):
        await ctx.send(':bangbang: This command cannot be used in PMs.')
    else:
        await ctx.send('An error has occurred... :disappointed:')
        log.error(f'Ignoring exception in command {ctx.command}')
        log.error(''.join(traceback.format_exception(type(err), err,
                err.__traceback__)))

# Sends the github link.
@bot.command()
async def source(ctx):
    await ctx.send(src_fork)
    await ctx.send(f'Forked from: {src}')

@bot.command()
async def help(ctx, page=None):
    info = help_page if not page or page == '1' else help_page_2
    await embed_help(ctx, 'Konichiwa welcome link start!', info)

# Bot sends a dm to creator with the name of the user and their request.
@bot.command()
async def request(ctx, feature):
    for cid in creator_id:
        creator = bot.get_user(cid)
        authors_name = str(ctx.author)
        await creator.send(f''':pencil: {authors_name}: {feature}''')
    await ctx.send(f''':pencil: Thanks, "{feature}" has been requested!''')

# Bot sends a dm to creator with the name of the user and their report.
@bot.command()
async def report(ctx, error_report):
    for cid in creator_id:
        creator = bot.get_user(cid)
        authors_name = str(ctx.author)
        await creator.send(f''':triangular_flag_on_post: {authors_name}: {error_report}''')
    await ctx.send(f''':triangular_flag_on_post: Thanks for the help, "{error_report}" has been reported!''')

# @bot.command()
# async def creator(ctx):
#     await ctx.send(creator_info)

@bot.command()
async def amicool(ctx):
    authors_name = str(ctx.author)
    
    if any((name in authors_name for name in cool_names)):
        await ctx.send('You are very cool')
    else:
        await ctx.send('lolno')
        await ctx.send('Psst, kid.  Want to be cool?  Find an issue and report it or request a feature you think would be cool.')



if __name__ == "__main__" :
     for extension in extensions:
        bot.load_extension('cogs.' + extension)
        bot.run(DISCORD_TOKEN)
        bot.run(auth_token)