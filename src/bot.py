import discord

client = discord.Client(intents=discord.Intents.default())

# client.run("TOKEN")

@client.event
async def on_ready():
    print("Le bot est prêt !")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.content)
