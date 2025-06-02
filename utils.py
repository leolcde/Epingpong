import sqlite3
import discord

def is_player_in_db(user_id: int) -> bool:
    conn = sqlite3.connect('elo_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM elo_data WHERE user_id = ?", (str(user_id),))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    return False

def ensure_player_is_in_db(player: discord.User):
    user_id = player.id
    if not is_player_in_db(player.id):
        conn = sqlite3.connect('elo_data.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO elo_data (id, user_id, elo) VALUES (?, ?, ?)", (str(user_id), str(user_id), 100))
        conn.commit()
        conn.close()
    return 0
