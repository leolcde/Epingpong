import discord
import json

class player_elo:
    def __init__(self, player_id, elo):
        self.id = player_id
        self.elo = elo

class player:
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    match_queue = []
    global_dict = {}
    p1 = None
    p2 = None

@player.client.event
async def on_ready():
    print("Le bot est carré mgl")
@player.client.event
async def on_message(message):
    if message.author == player.client.user:
        return
    # TO JOIN THE QUEUE
    if message.content == "!join":
        user_id = message.author.id
        if user_id not in player.match_queue:
            player.match_queue.append(user_id)
            await message.channel.send(f"{message.author.mention} a rejoint la file d'attente. Position : {len(player.match_queue)}")
        else:
            await message.channel.send(f"{message.author.mention}, tu es déjà dans la file d'attente.")

    # FOR DISPLAY THE QUEUE
    if message.content == "!queue":
        if player.match_queue:
            print(player.match_queue)
            queue_list = []
            for i, user_id in enumerate(player.match_queue):
                user = await player.client.fetch_user(user_id)
                if user is not None:
                    queue_list.append(f"{i+1}. {user.name}")
                else:
                    queue_list.append(f"{i+1}. Utilisateur inconnu")
            await message.channel.send(f"File d'attente actuelle :\n" + "\n".join(queue_list))
        else:
            await message.channel.send("La file d'attente est vide.")

    # FOR LEAVE THE QUEUE
    if message.content == "!leave":
        i = 0
        user_id = message.content
        if user_id in match_queue:
            while user_id != match_queue[i]:
                i += 1
            match_queue.pop(i)
            await message.channel.send(f"{message.autor.mention} a quitté la file d'attente.")
        else:
            await message.channel.send(f"{message.autor.mention}, tu n'es pas dans la file d'attente.")
client.run(discord_token)