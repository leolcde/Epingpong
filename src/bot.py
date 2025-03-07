import discord

client = discord.Client(intents=discord.Intents.default())

client.run("MTM0NzU4NjUzNDUyMTQzODI1Mg.GCNp-R.9olsKlnOxowvvnR4f7HoQYhrxkXtyb5KPCVykU")

@client.event
async def on_ready():
    print("Le bot est prêt !")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.content)
