import discord

discord_token = "TOKEN"
import discord

default_intents = discord.Intents.default()
client = discord.Client(intents=default_intents)

match_queue = []

@client.event
async def on_ready():
    print("le bot est carré mgl")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "!join":
        if message.author not in match_queue:
            match_queue.append(message.author)
            await message.channel.send(f"{message.author.mention} a rejoint la file d'attente. Position : {len(match_queue)}")
        else:
            await message.channel.send(f"{message.author.mention}, tu es déjà dans la file d'attente.")

client.run(discord_token)
