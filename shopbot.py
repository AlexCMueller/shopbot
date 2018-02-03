import asyncio
import botinfo
import discord
from discord.ext import commands
import io
import json
import requests
import time

url = "https://app.splatoon2.nintendo.net/api/onlineshop/merchandises"
urlshort = "https://app.splatoon2.nintendo.net"
cookies = {"iksm_session" : botinfo.iksm_session}

bot = commands.Bot(command_prefix='a?')

async def shop_task():
    await bot.wait_until_ready()
    while not bot.is_closed:
        r = requests.get(url, cookies=cookies)
        merch = json.loads(r.text)["merchandises"]

        img = urlshort+merch[-1]["gear"]["image"]
        latest_gear = merch[-1]["gear"]
        
        embed = discord.Embed()
        embed.set_author(name=merch[-1]["gear"]["brand"]["name"],
                         icon_url=urlshort+merch[-1]["gear"]["brand"]["image"])
        embed.set_image(url=img)
        embed.add_field(name="Gear Name", value=merch[-1]["gear"]["name"])
        embed.add_field(name="Main Ability",
                        value=merch[-1]["skill"]["name"])
        embed.add_field(name="Common Sub",
                        value=latest_gear["brand"]["frequent_skill"]["name"])
        embed.add_field(name="Rarity", value=latest_gear["rarity"]+1)

        await bot.send_message(bot.get_channel("407665743581151242"),
                               embed=embed)

        update_time = merch[0]["end_time"] + 10
        current_time = time.time()

        await asyncio.sleep(update_time - current_time)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def ping(ctx):
    print(ctx.message.channel.id)
    await bot.say("pong")

bot.loop.create_task(shop_task())
bot.run(botinfo.token)
