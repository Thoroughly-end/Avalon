from discord.ext import commands
import discord
from discord import app_commands
from cogs.rules import rules
from cogs.view import view as gameview
import random

class basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games : dict[int, str] = {}
    
    @app_commands.command(name = 'start', description = 'Start a game')
    @app_commands.guild_only()
    async def start(self, interaction: discord.Interaction):
        assert interaction.channel_id is not None
        channel_id = interaction.channel_id

        if channel_id in self.active_games:
            await interaction.response.send_message("⚠️ 這裡已經有一個正在進行的遊戲了！", ephemeral = True)
            return
        
        self.active_games[channel_id] = "Lobby"

        try:
            view = gameview.GameView(author = interaction.user)
            embed = view.create_embed()
            await interaction.response.send_message(embed = embed, view = view)
            message = await interaction.original_response()
            view.message = message
            await view.wait()

            if view.status == "cancel":
                return
            
            if channel_id not in self.active_games:
                await interaction.followup.send("🛑 遊戲因指令被終止。")
                return
            
            if view.status == "start":
                self.active_games[channel_id] = "In Progress"
                await interaction.followup.send("🎲 正在進行角色分配...")
            
                final_players : list[discord.User | discord.Member] = view.players

                game = rules.Game(final_players = final_players)

                for player in final_players:
                    agent = game.search(player.id)
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
                        elif agent == "Assassin":
                            morgana = game.players.morgana.getPlayer()
                            msg = f"Your partner is {morgana.display_name}."
                            await player.send(msg)
                        
                    except discord.Forbidden:
                        await interaction.followup.send(f"❌ 無法私訊給 {player.mention}！請開啟伺服器私訊功能後重來。")
                        view.status = "cancel"
                        return
                
                for round in range(1, 6):
                    if channel_id not in self.active_games:
                        return
                    await self.mainFunc(interaction, final_players, game)
                    game.nextRound()
                    winner = game.checkWin()
                    if winner is None:
                        continue
                    elif winner == "justice":
                        await interaction.followup.send("⚔️ **正義陣營獲勝！**")
                        return
                    elif winner == "evil":
                        await interaction.followup.send("🗡️ **邪惡陣營獲勝！**")
                        return
                
        except Exception as e:
            await interaction.followup.send(f"💥 發生錯誤：{e}")
            raise e
            
        finally:
            if channel_id in self.active_games:
                del self.active_games[channel_id]
                print(f"頻道 {channel_id} 的遊戲狀態已清除")
        

    @app_commands.command(name = 'stop', description = 'Stop a game')
    async def stop(self, interaction: discord.Interaction):
        channel_id = interaction.channel_id

        if channel_id in self.active_games:
            del self.active_games[channel_id]
            await interaction.response.send_message("**🛑 遊戲已停止。**")
        else:
            await interaction.response.send_message("⚠️ 目前沒有正在進行的遊戲！", ephemeral = True)
    
    async def mainFunc(self,  interaction: discord.Interaction, players : list[discord.User | discord.Member], game : rules.Game):
        choosenPlayers = await self.choose(interaction, players, game)
        result = await self.vote(interaction, choosenPlayers, players)
        if result == True:
            await interaction.followup.send("✅ 投票通過！")
            missionResult = await self.mission(interaction, choosenPlayers, game)
            if missionResult == "success":
                await interaction.followup.send("🎉 任務成功！")
                game.missionSuccess()
            elif missionResult == "fail":
                await interaction.followup.send("💥 任務失敗！")
                game.missionFail()
            else:
                await interaction.followup.send("⚠️ 任務過程中發生錯誤，遊戲終止！")
                return
        
        elif result == False:
            await interaction.followup.send("❌ 投票失敗！換下一位國王！")
            game.objectionAdd()
            return
        
        else:
            await interaction.followup.send("⚠️ 超時未投票！流局！")
            return
        

        
    async def choose(self,  interaction: discord.Interaction, players : list[discord.User | discord.Member], game : rules.Game):
        view = gameview.ChooseView(king = game.getCurrentKing(game.round), players = players, num = game.getMissionNum())
        embed = view.create_embed()
        await interaction.followup.send(embed = embed, view = view)
        message = await interaction.original_response()
        view.message = message
        await view.wait()

        choosenPlayers : list[discord.User | discord.Member] = []
        for i in range(0, 6):
            if view.chooseList[i] == True:
                choosenPlayers.append(players[i])
        return choosenPlayers

    async def vote(self, interaction: discord.Interaction, choosenPlayers : list[discord.User | discord.Member], players : list[discord.User | discord.Member]):
        view = gameview.VoteView(players = players, choosenPlayers = choosenPlayers)
        embed = view.create_embed()
        await interaction.followup.send(embed = embed, view = view)
        message = await interaction.original_response()
        view.message = message
        await view.wait()
        return view.status
    
    async def mission(self, interaction: discord.Interaction, choosenPlayers : list[discord.User | discord.Member], game : rules.Game):
        viewList : list[gameview.MissionView] = []
        for player in choosenPlayers:
            try:
                view = gameview.MissionView(game, player)
                embed = view.create_embed()
                message = await player.send(embed = embed, view = view)
                view.message = message
                viewList.append(view)
            except discord.Forbidden:
                await interaction.followup.send(f"❌ 無法私訊給 {player.mention}！請開啟伺服器私訊功能後重來。")
                return "error"

        for view in viewList:
            await view.wait()
        for view in viewList:
            if view.status == False:
                return "fail"
        return "success"

        

async def setup(bot : commands.Bot):
    await bot.add_cog(basic(bot))