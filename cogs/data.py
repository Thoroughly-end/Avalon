from discord.ext import commands
import discord
from discord import app_commands
from cogs.view import view as gameview
import os
import json

class data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getWinMatches(player_id : int, players_data : list[dict]) -> int:
        win_matches = 0
        for record in players_data:
            if record["player_id"] == player_id:
                win_matches = record["win_matches"]
                break
        return win_matches
        
    def getLossMatches(player_id : int, players_data : list[dict]) -> int:
        loss_matches = 0
        for record in players_data:
            if record["player_id"] == player_id:
                loss_matches = record["loss_matches"]
                break
        return loss_matches
    
    def getExsitedPlayersIDs(players_data : list[dict]) -> list[int]:
        ids : list[int] = []
        for record in players_data:
            ids.append(record["player_id"])
        return ids
    
    @app_commands.command(name = "profile", description = "Check your win rates")
    @app_commands.guild_only()
    async def profile(self, interaction : discord.Interaction):
        win_matches = 0
        loss_matches = 0
        win_rate = 0.0
        file = f"records/guide_{interaction.guild_id}_records.json"
        if os.path.exists(file):
            with open(file, "r") as f:
                records : dict = json.load(f)
                players_data : list[dict] = records["players_data"]
                win_matches = data.getWinMatches(interaction.user.id, players_data)
                loss_matches = data.getLossMatches(interaction.user.id, players_data)
                if win_matches + loss_matches > 0:
                    win_rate = win_matches / (win_matches + loss_matches) * 100
                else:
                    pass
        else:
            pass
        
        view = gameview.WinRateView(win_rate, win_matches, loss_matches, interaction)
        embed = view.create_embed()

        await interaction.response.send_message(embed = embed, view = view)

async def setup(bot : commands.Bot):
    await bot.add_cog(data(bot))