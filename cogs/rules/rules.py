from cogs.rules import characters
import discord
import random

class Game:
    def __init__(self, final_players : list[discord.User | discord.Member]):
        random.shuffle(final_players)
        self.players = characters.Players(final_players)
        self.final_players = final_players
    

    def search(self, id : str):
        for i in range(0, 6):
            if str(self.final_players[i].id) == id:
                if i == 0:
                    return "Merlin"
                if i == 1:
                    return "Percival"
                if i == 2 or i == 3:
                    return "LoyalServant"
                if i == 4:
                    return "Assassin"
                if i == 5:
                    return "Morgana"
        return "error"