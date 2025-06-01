import json
import discord

from gameManager import gameManager
from player_elo import player_elo


def change_elo(player1: discord.User, player2: discord.User):
    if player1.name in gameManager.global_dict:
        gameManager.global_dict[player1.name] += 10
    user1 = player_elo(player1.name, gameManager.global_dict[player1.name])
    write_on_json(user1)
    if player2.name in gameManager.global_dict:
        gameManager.global_dict[player2.name] -= 10
    user2 = player_elo(player2.name, gameManager.global_dict[player2.name])
    write_on_json(user2)
    return 0

def write_on_json(variable: player_elo):
    dictionary = {variable.id: variable.elo}
    gameManager.global_dict.update(dictionary)
    json_object = json.dumps(gameManager.global_dict)
    with open("elo_data.json", "w") as outfile:
        outfile.write(json_object)
        outfile.write("\n")
    return 0

def check_already_played(id: str):
    i = 0
    with open("elo_data.json", "r") as openfile:
        json_object = json.load(openfile)
        if list(json_object.values())[i] == id:
            return 0
        i += 1
    return 84

def check_players(player_name: str):
    if check_already_played(player_name) == 84:
        user = player_elo(player_name, 100)
        write_on_json(user)
    return 0
