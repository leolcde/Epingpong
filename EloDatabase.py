import sqlite3

create_table = """
CREATE TABLE IF NOT EXISTS elo_data (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    elo INTEGER NOT NULL DEFAULT 100,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

class EloDatabase:
    def __init__(self):
        # Remove self.conn and self.cursor
        conn = sqlite3.connect('elo_data.db')
        cursor = conn.cursor()
        cursor.execute(create_table)
        conn.commit()
        conn.close()

    def get_elo(self, user_id: str) -> int:
        conn = sqlite3.connect('elo_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT elo FROM elo_data WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
        return -1
    
    def update_elo(self, user_id: str, new_elo: int):
        conn = sqlite3.connect('elo_data.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE elo_data SET elo = ? WHERE user_id = ?", (new_elo, user_id))
        conn.commit()
        conn.close()

    def insert_player(self, user_id: str, elo: int = 100):
        conn = sqlite3.connect('elo_data.db')
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO elo_data (user_id, elo) VALUES (?, ?)", (user_id, elo))
        conn.commit()
        conn.close()

    def change_elo(self, winner_id: str, looser_id: str):
        self.insert_player(winner_id)
        self.insert_player(looser_id)

        winner_elo = self.get_elo(winner_id)
        looser_elo = self.get_elo(looser_id)

        new_winner_elo = winner_elo + 10
        new_looser_elo = looser_elo - 10

        self.update_elo(winner_id, new_winner_elo)
        self.update_elo(looser_id, new_looser_elo)
    
    def get_leaderboard(self) -> dict[str, int]:
        conn = sqlite3.connect('elo_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, elo FROM elo_data ORDER BY elo DESC")
        rows = cursor.fetchall()
        conn.close()
        return {row[0]: row[1] for row in rows}
