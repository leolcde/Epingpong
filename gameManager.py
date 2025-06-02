import os
import discord
import redis

from EloDatabase import EloDatabase

class GameManager:
    intents = discord.Intents.default()
    intents.message_content = True
    client : discord.Client = discord.Client(intents=intents)
    match_queue = []
    global_dict: dict[str, int] = {}
    elo_db = EloDatabase()

    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 0)),
        password=os.getenv("REDIS_PASSWORD", None)
    )

    def set_game_started(self):
        if self.redis_client.get("game_started") is None:
            self.redis_client.set("game_started", "true")
        print("Game started set in Redis")

            
    ## return a tuple with the two players elo scores
    def set_game_ended(self, winner: discord.User, looser: discord.User) -> tuple[int, int]:
        if self.redis_client.get("game_started") is not None:
            self.redis_client.delete("game_started")
        self.elo_db.change_elo(winner_id=str(winner.id), looser_id=str(looser.id))
        winner_elo = self.elo_db.get_elo(str(winner.id))
        looser_elo = self.elo_db.get_elo(str(looser.id))
        return winner_elo, looser_elo

    def is_game_started(self) -> bool:
        return self.redis_client.get("game_started") is not None
    
    def set_players(self, p1: discord.User, p2: discord.User):
        self.redis_client.set("p1", str(p1.id))
        self.redis_client.set("p2", str(p2.id))

    async def get_players(self) -> tuple[discord.User, discord.User]:
        p1_id = self.redis_client.get("p1")
        p2_id = self.redis_client.get("p2")
        p1 = await self.client.fetch_user(int(p1_id)) # type: ignore
        p2 = await self.client.fetch_user(int(p2_id)) # type: ignore
        return p1, p2

gameManager = GameManager()
