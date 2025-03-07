import discord

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print("Le bot est prêt !")

@client.event
async def on_message(message):
    print(message.content)

# put token here .