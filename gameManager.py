import discord

class gameManager:
    intents = discord.Intents.default()
    intents.message_content = True
    client : discord.Client = discord.Client(intents=intents)
    match_queue = []
    global_dict: dict[str, int] = {}
    p1 : None | discord.User = None
    p2: None | discord.User = None
