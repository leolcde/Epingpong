import discord
import json

class player_elo:
    def __init__(self, player_id, elo):
        self.id = player_id
        self.elo = elo

class player:
    discord_token = "MTM0NzU4NjUzNDUyMTQzODI1Mg.GHLPFR.j40gTP0ko0OVaYLgpYmIb6GaW-1foTaYOBLB-Y"
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    match_queue = []
    @client.event
    async def on_ready():
        print("Le bot est carré mgl")
    @client.event
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
        user_id = message.author.id
        if user_id in player.match_queue:
            while user_id != player.match_queue[i]:
                i += 1
            player.match_queue.pop(i)
            await message.channel.send(f"{message.author.mention} a quitté la file d'attente.")
        else:
            await message.channel.send(f"{message.author.mention}, tu n'es pas dans la file d'attente.")

def write_on_json(variable):
    dictionary = {variable.id: variable.elo}
    json_object = json.dumps(dictionary, indent=1)
    with open("elo_data.json", "w") as outfile:
        outfile.write(json_object)
    return 0

def check_already_played(id):
    i = 0
    with open("elo_data.json", "r") as openfile:
        json_object = json.load(openfile)
        if json_object.values(i) == id:
            return 0
        i += 1
    return 84

def check_players():
    user = player_elo()
    if check_already_played(player.message.author.id) == 84:
        user = (player.message.author.id, 100)
        write_on_json(user)
    return 0

player.client.run(player.discord_token)