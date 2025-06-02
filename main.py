import os
import sys
import discord
from dotenv import load_dotenv
from gameManager import gameManager
from utils import ensure_player_is_in_db
from RedisMatchQueue import RedisMatchQueue

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
tree = discord.app_commands.CommandTree(gameManager.client)

match_queue = RedisMatchQueue(
    redis_client=gameManager.redis_client,
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
    if not gameManager.is_game_started():
        await interaction.response.send_message(
            "No match in progress. Please start a match first.", ephemeral=True
        )
        return
    p1, p2 = await gameManager.get_players()

    class WinnerView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=30)

        async def update_message(self, interaction_button: discord.Interaction, winner: discord.User, looser: discord.User):
            gameManager.set_game_ended(winner=winner, looser=looser)
            await interaction_button.response.edit_message(
                content=f"<@{winner.id}> est le gagnant! ELO mis à jour.",
                view=None
            )

        @discord.ui.button(label=p1.name, style=discord.ButtonStyle.primary)
        async def p1_button(self, interaction_button: discord.Interaction, button: discord.ui.Button): # type: ignore
            await self.update_message(interaction_button, winner=p1, looser=p2)
            self.stop()

        @discord.ui.button(label=p2.name, style=discord.ButtonStyle.danger)
        async def p2_button(self, interaction_button: discord.Interaction, button: discord.ui.Button): # type: ignore
            await self.update_message(interaction_button, winner=p2, looser=p1)
            self.stop()

    await interaction.response.send_message(
        "Cliquez sur le nom du gagnant :", view=WinnerView()
    )


@tree.command(name="ranking", description="Afficher le classement ELO")
async def ranking(interaction: discord.Interaction):
    leaderboard = gameManager.elo_db.get_leaderboard()
    if not leaderboard:
        await interaction.response.send_message("Le classement est vide.", ephemeral=True)
        return
    sorted_leaderboad : dict[str, int] = {}
    for user_id, elo in leaderboard.items():
        user = await gameManager.client.fetch_user(int(user_id))
        sorted_leaderboad[user.name] = elo
    leaderboard_result = "\n".join([f"{name}: {elo}" for name, elo in sorted_leaderboad.items()])
    embed = discord.Embed(
        title="Classement ELO",
        description=leaderboard_result,
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

# FOR JOIN THE QUEUE
@tree.command(name="join", description="Rejoindre la file d'attente")
async def join(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if not match_queue.contains(user_id):
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
    user_id = str(interaction.user.id)
    if match_queue.contains(user_id):
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
    queue = match_queue.get_all()
    print(f"Current queue: {queue}")  # Debugging line to check the queue contents
    if queue:
        queue_list : list[str] = []
        for i, user_id in enumerate(queue[:10]):
            try:
                user = await gameManager.client.fetch_user(int(user_id))
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
    print("Starting match...")
    if gameManager.is_game_started():
        await interaction.response.send_message(
            "Un match est déjà en cours. Veuillez attendre qu'il se termine.",
            ephemeral=True
        )
        return
    queue = match_queue.get_all()
    print(f"Current queue: {queue}")  # Debugging line to check the queue contents
    if len(queue) >= 2:
        user_id1 = int(match_queue.pop())  # type: ignore
        user_id2 = int(match_queue.pop())  # type: ignore
        p1 = await gameManager.client.fetch_user(user_id1) # type: ignore
        p2 = await gameManager.client.fetch_user(user_id2) # type: ignore
        gameManager.set_players(p1, p2)
        await interaction.response.send_message(
            f"Match en cours entre <@{p1.id}> et <@{p2.id}> !"
        )
        ensure_player_is_in_db(p1)
        ensure_player_is_in_db(p2)
        gameManager.set_game_started()
    else:
        await interaction.response.send_message(
            "Il n'y a pas assez de joueur pour lancer un match...",
            ephemeral=True
        )

token = os.getenv("DISCORD_TOKEN")
if token is None:
    print("Token not found. Please set DISCORD_TOKEN in your .env file.", file=sys.stderr)
    sys.exit(1)
else:
    print("Token found. Starting the bot...")


gameManager.client.run(token)
