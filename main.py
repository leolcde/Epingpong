import asyncio
import json
import sys
import discord
from dotenv import load_dotenv
import os
import redis
from gameManager import gameManager
from utils import change_elo, check_players
from RedisMatchQueue import RedisMatchQueue

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
tree = discord.app_commands.CommandTree(gameManager.client)
    
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0)),
    password=os.getenv("REDIS_PASSWORD", None)
)

match_queue = RedisMatchQueue(
    redis_client=redis_client,
    queue_name=os.getenv("REDIS_QUEUE_NAME", "match_queue")
)

@gameManager.client.event
async def on_ready():
    print("Le bot est carré mgl")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}", file=sys.stderr)

@tree.command(name="win", description="Déclarer le gagnant du match en cours")
async def win(interaction: discord.Interaction):
    if gameManager.p1 is None or gameManager.p2 is None:
        await interaction.response.send_message("No match in progress. Please start a match first.", ephemeral=True)
        return
    if gameManager.p1.name and gameManager.p2.name:
        await interaction.response.send_message(
            f"Who's the winner?\n> {gameManager.p1.name}\n> {gameManager.p2.name}\nRépondez par le nom exact du gagnant dans le chat."
        )
        def check(m: discord.Message):
            return (
                m.author == interaction.user and
                m.channel == interaction.channel
            )
        try:
            reply = await gameManager.client.wait_for('message', check=check, timeout=30)
            winner = reply.content.strip()
            if winner == gameManager.p1.name:
                change_elo(gameManager.p1, gameManager.p2)
                await interaction.followup.send(f"<@{gameManager.p1.id}> est le gagnant! ELO mis à jour.")
            elif winner == gameManager.p2.name:
                change_elo(gameManager.p2, gameManager.p1)
                await interaction.followup.send(f"<@{gameManager.p2.id}> est le gagnant! ELO mis à jour.")
            else:
                await interaction.followup.send("Nom invalide. Veuillez répondre avec le nom exact du gagnant.")
        except asyncio.TimeoutError:
            await interaction.followup.send("Temps écoulé pour répondre. Veuillez réessayer.")

@tree.command(name="ranking", description="Afficher le classement ELO")
async def ranking(interaction: discord.Interaction):
    with open("elo_data.json", "r") as openfile:
        gameManager.global_dict = json.load(openfile)
    leaderboard = "\n".join(
        f"{name}: {elo}" for name, elo in sorted(gameManager.global_dict.items(), key=lambda x: x[1], reverse=True)
    )
    await interaction.response.send_message(f"Leaderboard :\n{leaderboard}")

# FOR JOIN THE QUEUE
@tree.command(name="join", description="Rejoindre la file d'attente")
async def join(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id not in match_queue.get_all():
        match_queue.push(user_id)
        await interaction.response.send_message(
            f"{interaction.user.mention} a rejoint la file d'attente. Position : {len(match_queue.get_all())}."
        )
    else:
        await interaction.response.send_message(
            f"{interaction.user.mention}, tu es déjà dans la file d'attente.",
            ephemeral=True
        )

# FOR LEAVE THE QUEUE
@tree.command(name="leave", description="Quitter la file d'attente")
async def leave(interaction: discord.Interaction):
    user_id = interaction.user.id
    if not match_queue.contains(user_id):
        match_queue.push(user_id)
        await interaction.response.send_message(
            f"{interaction.user.mention} a quitté la file d'attente."
        )
    else:
        await interaction.response.send_message(
            f"{interaction.user.mention}, tu n'es pas dans la file d'attente.",
            ephemeral=True
        )

# FOR SHOW THE QUEUE
@tree.command(name="queue", description="Afficher la file d'attente")
async def queue(interaction: discord.Interaction):
    queue = match_queue.get_all()
    if queue:
        queue_list : list[str] = []
        for i, user_id in enumerate(queue):
            try:
                user = await gameManager.client.fetch_user(user_id)
                queue_list.append(f"{i+1}. {user.name}")
            except discord.NotFound:
                queue_list.append(f"{i+1}. Utilisateur inconnu")
        embed = discord.Embed(
            title="File d'attente",
            description="\n".join(queue_list),
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message("La file d'attente est vide.", ephemeral=True)

@tree.command(name="start", description="Démarrer un match")
async def start(interaction: discord.Interaction):
    queue = match_queue.get_all()
    if len(queue) >= 2:
        gameManager.p1 = await gameManager.client.fetch_user(match_queue.pop()) # type: ignore
        gameManager.p2 = await gameManager.client.fetch_user(match_queue.pop()) # type: ignore
        await interaction.response.send_message(
            f"Match en cours entre <@{gameManager.p1.id}> et <@{gameManager.p2.id}> !"
        )
        check_players(gameManager.p1.name)
        check_players(gameManager.p2.name)
    else:
        await interaction.response.send_message(
            "Il n'y a pas assez de joueur pour lancer un match..."
        )

token = os.getenv("DISCORD_TOKEN")
if token is None:
    print("Token not found. Please set DISCORD_TOKEN in your .env file.", file=sys.stderr)
    sys.exit(1)
else:
    print("Token found. Starting the bot...")


gameManager.client.run(token)
