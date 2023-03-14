from dis import dis
from time import time
from playerFiles.equipment import Equipment
from items import Item, noneItem
import playerFiles.player as player
import discord
import constant as const
from functions import getCurrentActionView, getItem, MyView, addItemToInv, getReward, getXpReward
from discord import Button, Emoji, Interaction
from datetime import datetime, timedelta
import embeds
import random


# /*/*/*/*/*/*/**/*/**/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/**/
# /*/*/*/*/*/*/*/*/ 【 Ｍｉｎｅ 】/*/*/*/*//*/*/*//*/**/*/*/

class Mine:
    def __init__(self, name: str, description: str, lootPerLayer: dict, lootList: list[Item], max_depth: int):
        self.name = name
        self.desc = description
        self.loot = lootPerLayer
        self.lootList = lootList
        self.max_depth = max_depth

    async def enter(self, ctx: discord.ext.commands.Context, equipment: Equipment, player: player.Profile):
        def getView():

            class Dropdown1(discord.ui.Select):
                def __init__(self, placeholder: str, min_values: int = 1, max_values: int = 1, disabled: bool = False):
                    super().__init__(placeholder=placeholder, min_values=min_values,
                                     max_values=max_values, disabled=disabled)

                async def callback(self, interaction: Interaction):
                    # new dropdown to answer and we are giving it the answer of the first dropdown
                    await interaction.response.edit_message(view=getSecondView(depth=self.values[0]))

            view = MyView()

            dropdown1 = Dropdown1(placeholder="Choose the depth")

            if 1 <= self.max_depth:
                dropdown1.add_option(
                    label="Depth 1", description="*Must be level **0** or above*", emoji="1️⃣", value="1")
            if 2 <= self.max_depth:
                dropdown1.add_option(
                    label="Depth 2", description="*Must be level **5** or above*", emoji="2⃣", value="2")

            view.add_item(dropdown1)

            return view

        def getSecondView(depth: str):

            class Dropdown2(discord.ui.Select):
                def __init__(self, placeholder: str, lootList: list[Item], mine_name: str, min_values: int = 1, max_values: int = 1, disabled: bool = False):
                    super().__init__(placeholder=placeholder, min_values=min_values,
                                     max_values=max_values, disabled=disabled)
                    self.lootList = lootList
                    self.mine_name = mine_name

                async def callback(self, interaction: Interaction):
                    # match case to get the reward based on time mined and the time until completion
                    rewards = []
                    xp_reward: int = 0
                    finish_time = datetime.now()
                    match self.values[0]:
                        case "1":   # 2 minutes
                            rewards = getReward(
                                nb_reward=1, possible_reward=self.lootList)
                            xp_reward = getXpReward(nb_xp=2)
                            finish_time = datetime.now() + timedelta(minutes=2)
                        case "2":   # 10 minutes
                            xp_reward = getXpReward(nb_xp=9)
                            rewards = getReward(
                                nb_reward=6, possible_reward=self.lootList)
                            finish_time = datetime.now() + timedelta(minutes=10)
                        case "3":   # 30 minutes
                            xp_reward = getXpReward(nb_xp=40)
                            rewards = getReward(
                                nb_reward=17, possible_reward=self.lootList)
                            finish_time = datetime.now() + timedelta(minutes=30)
                        case "4":   # 60 minutes
                            xp_reward = getXpReward(nb_xp=100)
                            rewards = getReward(
                                nb_reward=36, possible_reward=self.lootList)
                            finish_time = datetime.now() + timedelta(hours=1)
                        case _:
                            print("there is something wrong here")

                    # Disable the dropdown so the player cant choose another option
                    self.disabled = True
                    await interaction.response.edit_message(view=view)

                    # send information to player class about what player is doing and for until when and send reward if completed
                    player.current_Action["action"] = f"mining in `depth {depth}` at `{self.mine_name}`"
                    player.current_Action["finish_time"] = finish_time
                    player.current_Action["rewards"] = rewards
                    player.current_Action["xp_rewards"].append((player.experience.MINER_XP_TYPE, xp_reward))

                    await interaction.followup.send(embed=embeds.getCurrentActionEmbed(ctx=ctx, action=player.current_Action["action"],
                                                                                       time_until_ready=player.current_Action[
                                                                                           "finish_time"],
                                                                                       player_name=player.name),
                                                    view=getCurrentActionView(True, True, player=player))
                    print(player.current_Action["finish_time"])

            view = MyView()

            dropdown2 = Dropdown2(placeholder="Choose the time to spend in the mine",
                                  lootList=self.lootList, mine_name=self.name)
            dropdown2.add_option(label="2 minutes", emoji="⌛", value="1")
            dropdown2.add_option(label="10 minutes", emoji="⌛", value="2")
            dropdown2.add_option(label="30 minutes", emoji="⌛", value="3")
            dropdown2.add_option(label="60 minutes", emoji="⌛", value="4")

            view.add_item(dropdown2)

            return view

        def has_pickaxe(equip: Equipment):
            if equip.pickaxe.name == noneItem.name:
                return False
            return True

        if has_pickaxe(equip=equipment):
            await ctx.respond(embed=embeds.getMineEmbed(ctx, player, self.name, self.desc, self.lootList), ephemeral=True, view=getView())
        else:
            await ctx.respond(f"**{ctx.author.name}** you dont have a pickaxe!", ephemeral=True)


# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/
lootTableTestMine = {
    "1": {
        "Ruby": 10,
        "Diamond": 40,
        "Stone": 100
    }
}
testMine = Mine("⛩ Test Mine", "Ancient mine of time and contain test stone",
                lootTableTestMine, [getItem("0008"), getItem("0009"), getItem("0011")], 1)


# /*/*/*/*/*/*/**/*/**/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/**/
# /*/*/*/*/*/*/*/*/【 Ｆｉｓｈｉｎｇ 】/*/*/*/*//*/*/*//*/**/

class FishingSpot:
    def __init__(self, name: str, description: str, fishingTable: dict, lootList: list[Item]):
        self.name = name
        self.desc = description
        self.fishingTable = fishingTable
        self.lootList = lootList

    # fishing will be like your giving a list of task todo in a certain order and u must remember it and do it perfectly to catch the fish (harder fish = longer list)
    # Ex: [Pull, Pull, Pull, Pull, Let loose, Pull, Let loose, Pull, Catch]
    # Some fish need different bait etc

    async def enter(self, ctx: discord.ext.commands.Context, equipment: Equipment, player: player.Profile):

        def getView():

            class StartButton(discord.ui.Button):
                def __init__(self, label: str):
                    super().__init__(style=discord.ButtonStyle.green, label=label)

                async def callback(self, interaction: Interaction):
                    embedFishing = getEmbedFishing()
                    await interaction.response.edit_message(embed=embedFishing, view=getViewWhenFishing(embedFishing))

            view = MyView(timeout=120)
            view.add_item(StartButton("Enter"))
            return view

        def getViewWhenFishing(whenFishingEmbed: discord.Embed):

            class StartFishing(discord.ui.Button):
                def __init__(self, label: str, table: dict):
                    super().__init__(style=discord.ButtonStyle.green, label=label)
                    self.table = table

                async def callback(self, interaction: Interaction):
                    reward = randomReward(table=self.table)
                    actions = getActions(reward=reward)

                    # get the actions list in a string to display it on the embed.
                    actionsStr: str = ""
                    cpt = 1
                    for i in actions:
                        if cpt != len(actions):
                            actionsStr += f"[{i}] - "
                        else:
                            actionsStr += f"[{i}]"
                        cpt += 1

                    whenFishingEmbed.add_field(
                        name="You are feeling something on the line..", value=f"{actionsStr}")
                    await interaction.response.edit_message(embed=whenFishingEmbed, view=view)

            view = MyView(timeout=280)
            view.add_item(StartFishing(
                "Start Fishing", table=self.fishingTable))
            return view

        def getEmbedFishing():
            embed = discord.Embed(
                title=f">>> {self.name}", description=f"🎣**Fishing Rod** | {equipment.fishing_rod.display()}")
            return embed

        def randomReward(table: dict):
            reward = random.choice(range(1, 101))
            for k, v in table.items():
                if v <= reward:
                    return k

        def getActions(reward: str):
            actionsChoices: list = ["Pull", "Let loose"]
            actionsList = []
            rewardItem: Item
            for i in self.lootList:
                if i.simple_name == reward:
                    rewardItem = i

            # Depending on rarity, actions will be harder and longer
            rarityActions: dict = {
                "commun": 5,
                "rare": 10
            }
            cpt = 0
            while cpt < rarityActions[f"{rewardItem.rarity}"]:
                actionsList.append(random.choice(actionsChoices))
                cpt += 1

            return actionsList

        def has_fishingRod():
            if equipment.fishing_rod.name == noneItem.name:
                return False
            return True

        def lootListToString():
            string = ""
            for i in self.lootList:
                string += f"{i.display()} | "
            return string

        if has_fishingRod():
            embed = discord.Embed(
                title=f">>> {self.name}", description=f"{self.desc}")
            embed.add_field(name="Possible Loot",
                            value=f"{lootListToString()}")
            await ctx.respond(embed=embed, ephemeral=True, view=getView())
        else:
            await ctx.respond(f"**{ctx.author.name}** you dont have a fishing rod!", ephemeral=True)


# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/
testFishingTable = {
    "Star Fish": 10,
    "Shark": 40,
    "Salmon": 100
}

testFishingSpot = FishingSpot("Test Spot", "Basic oasis to fish peacefully", testFishingTable, [
                              getItem("0013"), getItem("0014"), getItem("0015")])
