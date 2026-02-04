from discord.ext import commands
import discord
from discord import app_commands
from cogs.rules import rules
from cogs.view import view as gameview
import random

class basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.inGame = False

    @app_commands.command(name = 'start', description = 'Start a game')
    async def start(self, interaction: discord.Interaction):
        view = gameview.GameView(author=interaction.user)
        embed = view.create_embed()
        await interaction.response.send_message(embed = embed, view = view)
        await view.wait()

        if view.status == "cancel":
            return
        if view.status == "start":
            await interaction.followup.send("🎲 正在進行角色分配...")
        
            final_players : list[discord.User | discord.Member] = view.players
            
            
            game = rules.Game(final_players = final_players)

            for player in final_players:
                agent = game.search(str(player.id))
                try:
                    embed = discord.Embed(
                        title = "你的身份是...",
                        description = f"# **{agent}**",
                        color = discord.Color.gold() if "Merlin" in agent or "LoyalServant" in agent or "Percival" in agent else discord.Color.red()
                    )
                    embed.set_footer(text = "請勿讀出你的身份！")

                    await player.send(embed = embed)

                    if agent == "Merlin":
                        assassin = game.players.assassin.getPlayer()
                        morgana = game.players.morgana.getPlayer()
                        arr = [assassin, morgana]
                        random.shuffle(arr)
                        msg = f"The evil is {arr[0].display_name} and {arr[1].display_name}. "
                        await player.send(msg)
                    elif agent == "Percival":
                        merlin = game.players.merlin.getPlayer()
                        morgana = game.players.morgana.getPlayer()
                        arr = [merlin, morgana]
                        random.shuffle(arr)
                        msg = f"{arr[0].display_name} and {arr[1].display_name}. One is Merlin, the other is Morgana."
                        await player.send(msg)
                    elif agent == "Morgana":
                        assassin = game.players.assassin.getPlayer()
                        msg = f"Your partner is {assassin.display_name}."
                        await player.send(msg)
                    elif agent == "assassin":
                        morgana = game.players.morgana.getPlayer()
                        msg = f"Your partner is {morgana.display_name}."


                except discord.Forbidden:
                    await interaction.followup.send(f"❌ 無法私訊給 {player.mention}！請開啟伺服器私訊功能後重來。")
                    view.status = "cancel"
                    return
            
            self.inGame = True
            await self.mainFunc(interaction, final_players)

    @app_commands.command(name = 'cancel', description = 'Cancel a game')
    async def cancel(self, interaction: discord.Interaction):
        if(self.inGame == False):
            await interaction.response.send_message("❌ 遊戲還沒開始。")
        else:
            self.inGame = False
    
    async def mainFunc(self,  interaction: discord.Interaction, players : list[discord.User | discord.Member]):
        await self.choose(interaction, players)
        if self.inGame == False:
            return

    async def choose(self,  interaction: discord.Interaction, players : list[discord.User | discord.Member]):
        view = gameview.ChooseView(king = players[0], players = players, num = 2)
        embed = view.create_embed()
        await interaction.followup.send(embed = embed, view = view)
        await view.wait()

        choosenPlayer : list[discord.User | discord.Member] = []
        for i in range(0, 6):
            if view.chooseList[i] == True:
                choosenPlayer.append(players[i])
        return choosenPlayer




        

async def setup(bot : commands.Bot):
    await bot.add_cog(basic(bot))