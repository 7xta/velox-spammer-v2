############################################################################                                                                    
#__   _____| | _____  __  ___ _ __   __ _ _ __ ___  _ __ ___   ___ _ __    #
#\ \ / / _ \ |/ _ \ \/ / / __| '_ \ / _` | '_ ` _ \| '_ ` _ \ / _ \ '__|   #
# \ V /  __/ | (_) >  <  \__ \ |_) | (_| | | | | | | | | | | |  __/ |      #
#  \_/ \___|_|\___/_/\_\ |___/ .__/ \__,_|_| |_| |_|_| |_| |_|\___|_|      #
#                            |_|                                           #
############################################################################
# developers: velox LyS s1f
# tester: s3b11



import discord
from discord.ext import commands, tasks
import asyncio
import sys
import multiprocessing
import requests
import time
import random
import threading
from colorama import Fore, Style
import fade
import socket
import os
import aiohttp
import subprocess
import psutil
import json
import tqdm
import ctypes
# from ctypes import windll

# script version


script_version = "VELOX SPAMMER V2"
sefi = "velox, LyS, s1f"






def ofutpemata(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path}  nu exista")

    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def samacacpetn(tokens):
    valid_tokens = [token.strip() for token in tokens if isinstance(token, str) and len(token.strip()) > 0]
    invalid_tokens = [token for token in tokens if token not in valid_tokens]
    return valid_tokens, invalid_tokens

def samacacpetn5(tokens, filename):
    if tokens:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("\n".join(tokens))

def samacacpetn3(tokens, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for index, token in enumerate(tokens, start=1):
            file.write(f'{index}. {token}\n')

try:
    tokens = ofutpemata('tokens.txt')
    
    if not tokens:
        raise ValueError("n au fost gasite tokenuri in tokens.txt")

    valid_tokens, invalid_tokens = samacacpetn(tokens)
    
    samacacpetn5(valid_tokens, 'valid.txt')
    samacacpetn5(invalid_tokens, 'invalid.txt')

    if valid_tokens:
        samacacpetn3(valid_tokens, 'users.txt')

    main_token = valid_tokens[0] if valid_tokens else None

    if not main_token:
        raise ValueError("tokenuri valide n au fost gasite")


except Exception as e:
    print(f"eroare {e}")
    main_token = None 


intents = discord.Intents.default()
intents.presences = True
intents.guilds = True
intents.typing = True
intents.dm_messages = True
intents.messages = True
intents.members = True
guild_voice_states = True


#prefixe                                 
comenzi_prefix='$',                                                 
stream_prefix='#', 
client_streaming = commands.Bot(command_prefix=stream_prefix,self_bot=True,intents=intents)
bot = commands.Bot(command_prefix=comenzi_prefix, self_bot=True, intents=intents)

single_line_spam_messages = []
multi_line_spam_messages = []
repeated_message_spam_channels = {}
spiced_multi_line_spam_messages = []

single_line_spam_active = False
multi_line_spam_active = False
repeated_message_spam_active = False
spiced_multi_line_spam_active = False

single_line_spam_delay = 7
multi_line_spam_delay = 3
repeated_message_spam_delay = 5
spiced_multi_line_spam_delay = 3




def info(token):
    headers = {"Authorization": token}
    try:
        r = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if r.status_code == 200:
            user_data = r.json()
            return {
                "username": user_data.get("username", "Unknown"),
                "discriminator": user_data.get("discriminator", "0000"),
                "id": user_data.get("id", "N/A"),
                "nitro_status": "Yes" if user_data.get("premium_type", 0) != 0 else "No"
            }
        else:
            return {
                "username": "Unknown",
                "discriminator": "0000",
                "id": "N/A",
                "nitro_status": "Unknown"
            }
    except Exception as e:
        return {
            "username": "Error",
            "discriminator": "0000",
            "id": "N/A",
            "nitro_status": str(e)
        }



if main_token:
    infoslbz = info(main_token)

    mainfo = f"  script version {script_version} - Made by {sefi}"
    descinfo = f"""  SelfBot Informations:
  Version: {script_version}
  Logged in as: {infoslbz['username']}#{infoslbz['discriminator']}
  Nitro Status: {infoslbz['nitro_status']}
  User ID: {infoslbz['id']}"""

    print(fade.purplepink(mainfo))
    print(fade.purplepink(descinfo))


    def interpolate_color(start_color, end_color, t):
        start_hsv = [c / 255.0 for c in start_color]
        end_hsv = [c / 255.0 for c in end_color]
        interpolated_hsv = [
            start + t * (end - start) for start, end in zip(start_hsv, end_hsv)
        ]
        return tuple(int(c * 255) for c in interpolated_hsv)

    def custom_loading_bar(number, start_color, end_color):
        t = number / 200.0
        color = interpolate_color(start_color, end_color, t)
        color_code = f"\x1b[38;2;{color[0]};{color[1]};{color[2]}m"
        bar_length = 70
        bar = f"[{'#' * (number * bar_length // 200)}{' ' * (bar_length - (number * bar_length // 200))}]"
        return f"{color_code}{bar} {number}%\x1b[31m"

    total_numbers = 200
    color_combinations = [((80, 0, 255), (255, 0, 0))]
    for start_color, end_color in color_combinations:
        for i in range(1, total_numbers + 1):
            print(custom_loading_bar(i, start_color, end_color), end="\r")
            time.sleep(0.01)
#---------------------comenzi---------------------


#uptime
timestart = time.time()

@bot.command()
async def uptime(ctx):
    timp = time.time() - timestart
    zile = int(timp // (24 * 3600))
    timp = timp % (24 * 3600)
    ore = int(timp // 3600)
    timp %= 3600
    minute = int(timp // 60)
    secunde = int(timp % 60)
      
    await ctx.send(f'UPTIME {zile} zile, {ore} ore, {minute} minute, {secunde} secunde')

#sendfile
def load_messages(file_name):
    if not os.path.exists(file_name):
        raise FileNotFoundError
    with open(file_name, 'r') as file:
        return file.readlines()

@bot.command()
async def sendfile(ctx, file_name=None):
    await ctx.message.delete()

    if not file_name:
        return

    try:
        messages = list(load_messages(file_name))
    except FileNotFoundError:
        return

    if os.path.exists(file_name):
        await ctx.send(file=discord.File(f"{file_name}"))

#serverbanner
@bot.command()
async def serverbanner(ctx):
    await ctx.message.delete()
    if not ctx.guild.icon_url:
        await ctx.send(f"`server has no banner`")
        return
    await ctx.send(ctx.guild.banner_url) 


# iplookup

@bot.command()
async def iplookup(ctx, ip):
    api_key = "a91c8e0d5897462581c0c923ada079e5"
    api_url = f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip}"
    response = requests.get(api_url)
    data = response.json()
    await ctx.message.delete()
    if "country_name" in data:
        country = data["country_name"]
        city = data["city"]
        isp = data["isp"]
        current_time_unix = data["time_zone"]["current_time_unix"]
        current_time_formatted = f"<t:{int(current_time_unix)}:f>"
        message = f"# **RESULTS FOR IP** : {ip} \n **COUNTRY** : {country}\n **CITY** : {city}\n **ISP** : {isp}\n"
        await ctx.send(message)    


#serverav
@bot.command()
async def serverav(ctx): 
    await ctx.message.delete()
    if not ctx.guild.icon_url:
        await ctx.send(f"`server has no icon`")
        return
    await ctx.send(ctx.guild.icon_url)

@bot.command()  # count from to
async def afkcheck(ctx, arg1, arg2):
    await ctx.message.delete()
    ffrom = int(arg1)
    ffrom += 1
    fto = int(arg2)

    irange = fto - ffrom
    irange += 1

    for c in range(irange):
        num = c + ffrom
        await ctx.send(num)
#av
@bot.command()
async def av(ctx, user: discord.User):
    avatar_url = user.avatar_url
    await ctx.send(avatar_url)
    await ctx.message.delete()
#stream
@bot.command(description="up")
async def stream(ctx, *, game: str):
    await bot.change_presence(
        activity=discord.Streaming(name=game, url="https://smecherii.vercel.app/")
    )
    await ctx.message.delete()
#stopstream
@bot.command()
async def stopstream(ctx):
    await bot.change_presence(activity=None)
    await ctx.message.delete()
#massreact
@bot.command()
async def massreact(ctx, number=None, emote=None):
    number = int(number)
    await ctx.message.delete()
    messages = await ctx.message.channel.history(limit=number).flatten()
    for message in messages:
        try:
            await message.add_reaction(emote)
        except Exception:
            continue

@bot.command()
async def react(ctx, emoji: str = None):



    bot.monkreact = emoji


@bot.event
async def on_message(message):

    if message.author == bot.user:

        if hasattr(bot, 'monkreact'):
            try:
                await message.add_reaction(bot.monkreact)
            except:
                print(f"nu merge sa dea react {bot.monkreact}")


    await bot.process_commands(message)

#delay        
@bot.command()
async def delay(ctx, seconds: int):
    global delay
    delay = seconds
    await ctx.send(f"Delay set to {delay} seconds.")        
#startfile        
@bot.command()
async def startfile(ctx, filename: str):
        with open(filename, 'r') as file:
            messages = file.readlines()
        
        while True:
            for message in messages:
                await ctx.send(message.strip())
                await asyncio.sleep(delay) 


#vedem dak porneste
if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    async def main():
        await asyncio.gather(
            bot.start(main_token, bot=False),
            client_streaming.start(main_token, bot=False)
        )

    loop.run_until_complete(main()) 







