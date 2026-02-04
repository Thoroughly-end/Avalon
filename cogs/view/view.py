import discord
from discord import app_commands
class GameView(discord.ui.View):
    def __init__(self, author):
        super().__init__(timeout = None)
        self.players : list[discord.User | discord.Member] = []
        self.host : discord.Member = author
        self.players.append(author)
        self.status = None

    def create_embed(self):
        desc = "點擊下方按鈕加入遊戲！\n\n**目前玩家列表：**\n"
        if not self.players:
            desc += "*(暫無玩家)*"
        else:
            for i, p in enumerate(self.players, 1):
                desc += f"{i}. {p.display_name}\n"
        embed = discord.Embed(
            title = "🏰 阿瓦隆遊戲大廳",
            description = desc,
            color = discord.Color.blue()
        )
    
        embed.set_thumbnail(url = f"https://static.wikia.nocookie.net/colorbeeboardgame/images/6/6f/%E9%98%BF%E7%93%A6%E9%9A%86.jpg/revision/latest?cb=20161007095350&path-prefix=zh")
        embed.set_footer(text = f"由 {self.host.display_name} 發起 | 目前人數: {len(self.players)}")
        return embed
    
    @discord.ui.button(label = "join", style = discord.ButtonStyle.green)
    @app_commands.guild_only()
    async def join_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self.players:
            await interaction.response.send_message("❌ 你已經在列表裡了！", ephemeral=True)
            return
        
        self.players.append(interaction.user)
        await interaction.response.edit_message(embed = self.create_embed(), view=self)
    
    @discord.ui.button(label = "leave", style = discord.ButtonStyle.red)
    @app_commands.guild_only()
    async def leave_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.players:
            await interaction.response.send_message("❌ 你還沒加入！", ephemeral = True)
            return

        self.players.remove(interaction.user)
        await interaction.response.edit_message(embed = self.create_embed(), view = self)
    
    @discord.ui.button(label = "start", style = discord.ButtonStyle.blurple)
    @app_commands.guild_only()
    async def start_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.host:
            await interaction.response.send_message("⚠️ 只有開局者 (Host) 可以開始遊戲！", ephemeral = True)
            return

        if len(self.players) != 6:
            await interaction.response.send_message(f"⚠️ 人數錯誤！目前有 {len(self.players)} 人，需要 6 人。", ephemeral=True)
            return
        
        self.status = "start"
        await interaction.response.edit_message(content="✅ **遊戲開始！正在分配角色...**", view = self)
        self.stop()

    @discord.ui.button(label = "end", style = discord.ButtonStyle.danger)
    @app_commands.guild_only()
    async def cancel_game(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.host:
            await interaction.response.send_message("⚠️ 只有房主可以解散大廳！", ephemeral = True)
            return

        self.status = "cancel"

        await interaction.response.edit_message(content = "🛑 **遊戲大廳已解散。**", view = None, embed = None)
        self.stop()


class ChooseView(discord.ui.View):
    def __init__(self, king : discord.User | discord.Member, players : list[discord.User | discord.Member], num):
        super().__init__(timeout = None)
        self.king = king
        self.players = players
        self.num = num
        self.chooseList : list[bool] = [False, False, False, False, False, False]

    def create_embed(self):
        desc = "**選擇出任務的人選:**\n"
        for i, p in enumerate(self.players, 1):
                desc += f"{i}. {p.display_name}\n"
        
        desc += "\n**已經選擇:**\n"
        for i in range(0, 6):
            if self.chooseList[i] == True:
                if i == 0:
                    desc += "1️⃣"
                if i == 1:
                    desc += "2️⃣"
                if i == 2:
                    desc += "3️⃣"
                if i == 3:
                    desc += "4️⃣"
                if i == 4:
                    desc += "5️⃣"
                if i == 5:
                    desc += "6️⃣"


        embed = discord.Embed(
            title = "出任務階段",
            description = desc,
            color = discord.Color.blue()
        )

        embed.set_thumbnail(url = "https://www.mactt.org/wpress/wp-content/uploads/2021/08/Our-Mission-Mactt.jpg")
        return embed
    
    def check(self):
        count = 0
        for element in self.chooseList:
            if element == True:
                count += 1
        
        if count != self.num:
            return False
        else:
            return True
    
    def kingCheck(self, interaction: discord.Interaction):
        if interaction.user.id != self.king.id:
            return False
        else:
            return True
        
    @discord.ui.button(label = "1️⃣", style = discord.ButtonStyle.green)
    async def player1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.kingCheck(interaction) == False:
            await interaction.response.send_message("⚠️ 只有國王可以選擇人選！", ephemeral = True)
            return
        
        if self.chooseList[0] == True:
            self.chooseList[0] = False
        else:
            self.chooseList[0] = True
        
        await interaction.response.edit_message(embed = self.create_embed(), view = self)
    
    @discord.ui.button(label = "2️⃣", style = discord.ButtonStyle.green)
    async def player2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.kingCheck(interaction) == False:
            await interaction.response.send_message("⚠️ 只有國王可以選擇人選！", ephemeral = True)
            return
        
        if self.chooseList[1] == True:
            self.chooseList[1] = False
        else:
            self.chooseList[1] = True
        await interaction.response.edit_message(embed = self.create_embed(), view = self)

    @discord.ui.button(label = "3️⃣", style = discord.ButtonStyle.green)
    async def player3(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.kingCheck(interaction) == False:
            await interaction.response.send_message("⚠️ 只有國王可以選擇人選！", ephemeral = True)
            return
        
        if self.chooseList[2] == True:
            self.chooseList[2] = False
        else:
            self.chooseList[2] = True
        await interaction.response.edit_message(embed = self.create_embed(), view = self)

    @discord.ui.button(label = "4️⃣", style = discord.ButtonStyle.green)
    async def player4(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.kingCheck(interaction) == False:
            await interaction.response.send_message("⚠️ 只有國王可以選擇人選！", ephemeral = True)
            return
        
        if self.chooseList[3] == True:
            self.chooseList[3] = False
        else:
            self.chooseList[3] = True
        await interaction.response.edit_message(embed = self.create_embed(), view = self)

    @discord.ui.button(label = "5️⃣", style = discord.ButtonStyle.green)
    async def player5(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.kingCheck(interaction) == False:
            await interaction.response.send_message("⚠️ 只有國王可以選擇人選！", ephemeral = True)
            return
        
        if self.chooseList[4] == True:
            self.chooseList[4] = False
        else:
            self.chooseList[4] = True
        await interaction.response.edit_message(embed = self.create_embed(), view = self)

    @discord.ui.button(label = "6️⃣", style = discord.ButtonStyle.green)
    async def player6(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.kingCheck(interaction) == False:
            await interaction.response.send_message("⚠️ 只有國王可以選擇人選！", ephemeral = True)
            return
        
        if self.chooseList[5] == True:
            self.chooseList[5] = False
        else:
            self.chooseList[5] = True
        await interaction.response.edit_message(embed = self.create_embed(), view = self)

    @discord.ui.button(label = "✅", style = discord.ButtonStyle.blurple)
    async def go(self, interaction: discord.Interaction, button:discord.ui.Button):
        if self.kingCheck(interaction) == False:
            await interaction.response.send_message("⚠️ 只有國王可以選擇人選！", ephemeral = True)
            return
        
        if self.check() == False:
            await interaction.response.send_message(f"⚠️ 人數錯誤！需要{self.num}個人。", ephemeral=True)
        else:
            await interaction.response.edit_message(content="✅ **人選確定！正在進行任務...**", view = self)
            self.stop()
