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

    # TO LEAVE THE QUEUE
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

    # TO DISPLAY THE QUEUE
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

    # TO START THE MATCH
    if message.content == "!start":
        if len(player.match_queue) >= 2:
            print(player.match_queue)
            player.p1 = await player.client.fetch_user(player.match_queue.pop(0))
            player.p2 = await player.client.fetch_user(player.match_queue.pop(0))
            await message.channel.send(f"Match en cours entre {player.p1.mention} et {player.p2.mention} !")
            check_players(player.p1.name)
            check_players(player.p2.name)
        else:
            await message.channel.send(f"Il n'y a pas assez de joueur pour lancer un match...")

    # TO PUT THE WINNER OF THE MATCH
    if message.content == "!win":
        if player.p1.name and player.p2.name:
            await message.channel.send(f"Who's the winner?\n> {player.p1.name}\n> {player.p2.name}")
            def check(m):
                return m.author == message.author and m.channel == message.channel
            try:
                reply = await player.client.wait_for('message', check=check, timeout=30)
                winner = reply.content.strip()
                if winner == player.p1.name:
                    change_elo(player.p1, player.p2)
                    await message.channel.send(f"{player.p1.name} wins! ELO updated.")
                elif winner == player.p2.name:
                    change_elo(player.p2, player.p1)
                    await message.channel.send(f"{player.p2.name} wins! ELO updated.")
                else:
                    await message.channel.send("Please enter a valid name.")
            except player.asyncio.TimeoutError:
                await message.channel.send("You took too long to reply.")


    # TO DISPLAY THE LEADER BOARD
    if message.content == "!ranking":
        with open("elo_data.json", "r") as openfile:
            player.global_dict = json.load(openfile)
        await message.channel.send(f"leader-board de con :")
        await message.channel.send(player.global_dict)

def change_elo(player1, player2):
    if player1.name in player.global_dict:
        player.global_dict[player1.name] += 10
    user1 = player_elo(player1.name, player.global_dict[player1.name])
    write_on_json(user1)
    if player2.name in player.global_dict:
        player.global_dict[player2.name] -= 10
    user2 = player_elo(player2.name, player.global_dict[player2.name])
    write_on_json(user2)
    return 0

def write_on_json(variable):
    dictionary = {variable.id: variable.elo}
    player.global_dict.update(dictionary)
    json_object = json.dumps(player.global_dict)
    with open("elo_data.json", "w") as outfile:
        outfile.write(json_object)
        outfile.write("\n")
    return 0

def check_already_played(id):
    i = 0
    with open("elo_data.json", "r") as openfile:
        json_object = json.load(openfile)
        if list(json_object.values())[i] == id:
            return 0
        i += 1
    return 84

def check_players(player):
    if check_already_played(player) == 84:
        user = player_elo(player, 100)
        write_on_json(user)
    return 0

player.client.run(player.discord_token)
