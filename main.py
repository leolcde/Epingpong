import asyncio
import json
import sys
import discord
from dotenv import load_dotenv
import os

from gameManager import gameManager
from utils import change_elo, check_players

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
match_queue : list[int] = []
tree = discord.app_commands.CommandTree(gameManager.client)

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
                await interaction.followup.send(f"{gameManager.p1.name} wins! ELO updated.")
            elif winner == gameManager.p2.name:
                change_elo(gameManager.p2, gameManager.p1)
                await interaction.followup.send(f"{gameManager.p2.name} wins! ELO updated.")
            else:
                await interaction.followup.send("Please enter a valid name.")
        except asyncio.TimeoutError:
            await interaction.followup.send("You took too long to reply.")

@tree.command(name="ranking", description="Afficher le classement ELO")
async def ranking(interaction: discord.Interaction):
    with open("elo_data.json", "r") as openfile:
        gameManager.global_dict = json.load(openfile)
    leaderboard = "\n".join(
        f"{name}: {elo}" for name, elo in sorted(gameManager.global_dict.items(), key=lambda x: x[1], reverse=True)
    )
    await interaction.response.send_message(f"Leaderboard :\n{leaderboard}")


@tree.command(name="ping", description="Répond avec Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

# FOR JOIN THE QUEUE
@tree.command(name="join", description="Rejoindre la file d'attente")
async def join(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id not in match_queue:
        match_queue.append(user_id)
        await interaction.response.send_message(
            f"{interaction.user.mention} a rejoint la file d'attente. Position : {len(match_queue)}"
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
    if user_id in match_queue:
        match_queue.remove(user_id)
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
    if match_queue:
        queue_list : list[str] = []
        for i, user_id in enumerate(match_queue):
            try:
                user = await gameManager.client.fetch_user(user_id)
                queue_list.append(f"{i+1}. {user.name}")
            except discord.NotFound:
                queue_list.append(f"{i+1}. Utilisateur inconnu")
        await interaction.response.send_message(
            "File d'attente actuelle :\n" + "\n".join(queue_list)
        )
    else:
        await interaction.response.send_message("La file d'attente est vide.")

@tree.command(name="start", description="Démarrer un match")
async def start(interaction: discord.Interaction):
    if len(match_queue) >= 2:
        gameManager.p1 = await gameManager.client.fetch_user(match_queue.pop(0))
        gameManager.p2 = await gameManager.client.fetch_user(match_queue.pop(0))
        await interaction.response.send_message(
            f"Match en cours entre {gameManager.p1} et {gameManager.p2} !"
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
