import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
match_queue = []

@client.event
async def on_ready():
    print("Le bot est carré mgl")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # FOR JOIN THE QUEUE
    if message.content == "!join":
        user_id = message.author.id
        if user_id not in match_queue:
            match_queue.append(user_id)
            await message.channel.send(f"{message.author.mention} a rejoint la file d'attente. Position : {len(match_queue)}")
        else:
            await message.channel.send(f"{message.author.mention}, tu es déjà dans la file d'attente.")

    # FOR LEAVE THE QUEUE
    if message.content == "!leave":
        i = 0
        user_id = message.author.id
        if user_id in match_queue:
            while user_id != match_queue[i]:
                i += 1
            match_queue.pop(i)
            await message.channel.send(f"{message.author.mention} a quitté la file d'attente.")
        else:
            await message.channel.send(f"{message.author.mention}, tu n'es pas dans la file d'attente.")

    # FOR DISPLAY THE QUEUE
    if message.content == "!queue":
        if match_queue:
            print(match_queue)
            queue_list = []
            for i, user_id in enumerate(match_queue):
                user = await client.fetch_user(user_id)
                if user is not None:
                    queue_list.append(f"{i+1}. {user.name}")
                else:
                    queue_list.append(f"{i+1}. Utilisateur inconnu")
            await message.channel.send(f"File d'attente actuelle :\n" + "\n".join(queue_list))
        else:
            await message.channel.send("La file d'attente est vide.")

client.run(discord_token)