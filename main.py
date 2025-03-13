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

@player.client.event
async def on_ready():
    print("Le bot est carré mgl")
@player.client.event
async def on_message(message):
    if message.author == player.client.user:
        return
    # FOR JOIN THE QUEUE
    if message.content == "!join":
        user_id = message.author.id
        if user_id not in player.match_queue:
            player.match_queue.append(user_id)
            await message.channel.send(f"{message.author.mention} a rejoint la file d'attente. Position : {len(player.match_queue)}")
        else:
            await message.channel.send(f"{message.author.mention}, tu es déjà dans la file d'attente.")

    # FOR LEAVE THE QUEUE
    if message.content == "!leave":
        i = 0
        user_id = message.author.id
        if user_id in player.match_queue:
            while user_id != player.match_queue[i]:
                i += 1
            player.match_queue.pop(i)
            await message.channel.send(f"{message.author.mention} a quitté la file d'attente.")
        else:
            await message.channel.send(f"{message.author.mention}, tu n'es pas dans la file d'attente.")

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

    # FOR START THE MATCH
    if message.content == "!start":
        if len(player.match_queue) >= 2:
            print(player.match_queue)
            player1 = await player.client.fetch_user(player.match_queue.pop(0))
            player2 = await player.client.fetch_user(player.match_queue.pop(0))
            await message.channel.send(f"Match en cours entre {player1.mention} et {player2.mention} !")
            check_players(player1.name)
            check_players(player2.name)
        else:
            await message.channel.send(f"Il n'y a pas assez de joueur pour lancer un match...")

def write_on_json(variable):
    dictionary = {variable.id: variable.elo}
    player.global_dict.append(dictionary)
    json_object = json.dumps(player.global_dict)
    with open("elo_data.json", "w") as outfile:
        outfile.write(json_object)
        outfile.write("\n")
    return 0

def check_already_played(id):
    i = 0
    with open("elo_data.json", "r") as openfile:
        if json.JSONDecodeError:
            return 84
        json_object = json.load(openfile)
        if json_object.values(i) == id:
            return 0
        i += 1
    return 84

def check_players(player):
    if check_already_played(player) == 84:
        user = player_elo(player, 100)
        write_on_json(user)
    return 0

player.client.run(player.discord_token)
