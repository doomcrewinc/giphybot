
import discord
import asyncio
import random
import requests
import io
import safygiphy

client = discord.Client()
g = safygiphy.Giphy()
YOUR_NAME = "YOUR_USER_ID"

minutes = 0
hour = 0

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----------')
    await client.change_presence(game=discord.Game(name="with berserkers.net"))


@client.event
async def on_message(message):
    if message.content.lower().startswith('?test'):
        await client.send_message(message.channel, "Test passed")

    if message.content.lower().startswith('?coin'): #Coinflip 50/50% heads or tails
        choice = random.randint(1,2)
        if choice == 1:
            await client.add_reaction(message, '🌑')
        if choice == 2:
            await client.add_reaction(message, '🌕')

    if message.content.startswith('?game') and message.author.id == YOUR_NAME:
        game = message.content[6:]
        await client.change_presence(game=discord.Game(name=game))
        await client.send_message(message.channel, "I have changed my status to {0}".format(game))

    if message.content.startswith('?img'):
        response = requests.get("https://media3.giphy.com/media/6C9CMGMFtzzbO/giphy.gif", stream=True)
        await client.send_file(message.channel, io.BytesIO(response.raw.read()), filename='img.gif', content='Test image.')

    if message.content.startswith('?uptime'):
        await client.send_message(message.channel, "`I've been online for {0} hours and {1} minutes {2}. `".format(hour, minutes, message.server))

    if message.content.startswith('?gif'):
        gif_tag = message.content[5:]
        rgif = g.random(tag=str(gif_tag))
        response = requests.get(
            str(rgif.get("data", {}).get('image_original_url')), stream=True
        )
        await client.send_file(message.channel, io.BytesIO(response.raw.read()), filename='video.gif')

    if message.content.startswith('?fun'):
        gif_tag = "fun"
        rgif = g.random(tag=str(gif_tag))
        response = requests.get(
            str(rgif.get("data", {}).get('image_original_url')), stream=True
        )
        await client.send_file(message.channel, io.BytesIO(response.raw.read()), filename='video.gif')


async def tutorial_uptime():
    await client.wait_until_ready()
    global minutes
    minutes = 0
    global hour
    hour = 0
    while not client.is_closed:
        await asyncio.sleep(60)
        minutes += 1
        if minutes == 60:
            minutes = 0
            hour += 1

client.loop.create_task(tutorial_uptime())
client.run('YOUR_TOKEN')
