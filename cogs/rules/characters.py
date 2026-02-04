import discord
class character:
    def __init__(self):
        self.camp = ""
        self.name = ""
        self.player : discord.User | discord.Member
    
    def getPlayer(self):
        return self.player

class Players:
    def __init__(self, players : list[discord.User | discord.Member]):
        self.merlin = Merlin(players[0])
        self.percival = Percival(players[1])
        self.loyalServant1 = LoyalServant(players[2])
        self.loyalServant2 =  LoyalServant(players[3])
        self.assassin = Assassin(players[4])
        self.morgana = Morgana(players[5])
        


class Merlin(character):
    def __init__(self, player : discord.User | discord.Member):
        super().__init__()
        self.camp = "justice"
        self.name = "Merlin"
        self.player = player

class Assassin(character):
    def __init__(self, player : discord.User | discord.Member):
        super().__init__()
        self.camp = "evil"
        self.name = "Assassin"
        self.player = player

class Percival(character):
    def __init__(self, player : discord.User | discord.Member):
        super().__init__()
        self.camp = "justice"
        self.name = "Percival"
        self.player = player

class LoyalServant(character):
    def __init__(self, player : discord.User | discord.Member):
        super().__init__()
        self.camp = "justice"
        self.name = "Loyal Servant"
        self.player = player

class Morgana(character):
    def __init__(self, player : discord.User | discord.Member):
        super().__init__()
        self.camp = "evil"
        self.name = "Morgana"
        self.player = player