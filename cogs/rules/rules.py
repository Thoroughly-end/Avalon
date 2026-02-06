from cogs.rules import characters
import discord
import random

class Game:
    def __init__(self, final_players : list[discord.User | discord.Member]):
        random.shuffle(final_players)
        self.players = characters.Players(final_players)
        self.final_players = final_players
        self.round = 1
        self.objection_times = 0
        self.missons : list[bool | None] = [None, None, None, None, None]
    

    def search(self, id : int):
        if self.players.merlin.player.id == id:
            return "Merlin"
        if self.players.percival.player.id == id:
            return "Percival"
        if self.players.loyalServant1.player.id == id or self.players.loyalServant2.player.id == id:
            return "LoyalServant"
        if self.players.assassin.player.id == id:
            return "Assassin"
        if self.players.morgana.player.id == id:
            return "Morgana"
        return "error"
    
    def getProfie(self, id : int):
        if self.players.merlin.player.id == id:
            return self.players.merlin
        if self.players.percival.player.id == id:
            return self.players.percival
        if self.players.loyalServant1.player.id == id:
            return self.players.loyalServant1
        if self.players.loyalServant2.player.id == id:
            return self.players.loyalServant2
        if self.players.assassin.player.id == id:
            return self.players.assassin
        if self.players.morgana.player.id == id:
            return self.players.morgana
        return None
    
    def getCurrentKing(self, round : int):
        index = (round - 1) % 6
        return self.final_players[index]
    
    def getMissionNum(self):
        if self.round == 1:
            return 2
        elif self.round == 2 or self.round == 4:
            return 3
        elif self.round == 3 or self.round == 5:
            return 4
        else:
            return -1
        
    def nextRound(self):
        self.round += 1

    def getRound(self):
        return self.round

    def objectionAdd(self):
        self.objection_times += 1
    
    def missionSuccess(self):
        self.missons[self.round - 1] = True

    def missionFail(self):
        self.missons[self.round - 1] = False

    def checkWin(self):
        if self.objection_times >= 5:
            return "evil"
        
        success_count = self.missons.count(True)
        fail_count = self.missons.count(False)

        if success_count >= 3:
            return "justice"
        elif fail_count >= 3:
            return "evil"
        else:
            return None