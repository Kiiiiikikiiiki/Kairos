from datetime import datetime, timedelta
from email.policy import default
import constant as const
import player
import items
import discord
import discord.ext.commands
from discord.ui import Button, View
from discord import Interaction, Message, SelectOption
import copy
from random import choice
import embeds


def getItemsFromInv(profile_id: str):
    """
    :return: itemsString(1) -> List in string of non-usable items
             usablesItemsString(2) -> List in string of usable items
    """
    plyer: player.Profile = const.PROFILE_DICT[f'{profile_id}']
    inv: list[items.Item] = plyer.inventory.inv
    itemsString = ""            # the items string that will be return at the end
    usablesItemsString = ""     # the usables items string that will be return at the end

    seenItems = []  # filter to know if an item as already been added to the string
    itemIdList = []  # list of all the item id in inv
    for i in inv:
        itemIdList.append(i.item_id)
    for i in inv:
        if i.simple_name not in seenItems:
            nbOfThatItem = itemIdList.count(i.item_id)
            if i.usable:
                usablesItemsString += f"[`{i.name} [{nbOfThatItem}]`]({const.URL} '{i.desc}') \n"
            else:
                itemsString += f"[`{i.name} [{nbOfThatItem}]`]({const.URL} '{i.desc}') \n"
            seenItems.append(i.simple_name)
    if itemsString == "":
        itemsString = "❌"
    if usablesItemsString == "":
        usablesItemsString = "❌"
    return itemsString, usablesItemsString


def addItemToInv(item: items.Item, plyer: player.Profile, nbOfThatItem: int):
    itemNameList = []
    for i in plyer.inventory.inv:
        itemNameList.append(i.simple_name)
    if plyer.inventory.currentInvSize() < plyer.inventory.inv_size or item.simple_name in list(map(lambda x: x.simple_name, plyer.inventory.inv)):
        cpt = 0
        while (cpt < nbOfThatItem):
            plyer.inventory.inv.append(item)
            print(item, item.item_id)
            cpt += 1
        return True
    return False


def itemToInv(player: player.Profile, item: items.Item, nbOfItem: int):
    cpt = 0
    while (cpt < nbOfItem):
        player.inventory.inv.append(item)
        cpt += 1


# Receive item function with button and view
class MyView(View):
    def __init__(self, timeout: float = 400):
        super().__init__(timeout=timeout)

    async def on_timeout(self):
        self.stop()


def receiveItems(user_id: int, itemList: list[items.Item], plyer: player.Profile, ctx: discord.ext.commands.Context):
    """
    :return: finalMsg(1) -> the message to send
             view(2)     -> the view with button to add with the finalMsg
    """

    class ItemButton(Button):
        def __init__(self, label, item: items.Item, plyer: player.Profile, user_id: int, ctx: discord.ext.commands.Context, nbOfItem):
            super().__init__(style=discord.ButtonStyle.gray, label=label, disabled=False)
            self.user_id = user_id
            self.ctx = ctx
            self.item = item
            self.plyer = plyer
            self.nbOfItem = nbOfItem

        async def callback(self, interaction: Interaction):
            if interaction.user.id == self.user_id:
                if addItemToInv(item=self.item, plyer=self.plyer, nbOfThatItem=self.nbOfItem):
                    self.disabled = True
                    await interaction.response.edit_message(view=view)
                else:
                    await self.ctx.respond("Not enough space in your inventory", ephemeral=True)

    seenItem = []
    itemIdList = []
    itemListStr = ""
    view = MyView()
    for i in itemList:
        itemIdList.append(i.item_id)
    for i in itemList:
        if i.simple_name not in seenItem:
            nbOfThatItem = itemIdList.count(i.item_id)
            itemListStr += f"[`{i.name} [{nbOfThatItem}]`]({const.URL} '{i.desc}') | "
            seenItem.append(i.simple_name)
            view.add_item(ItemButton(label=i.name, item=i, plyer=plyer,
                                     user_id=user_id, ctx=ctx, nbOfItem=nbOfThatItem))

    finalEmbed = discord.Embed(
        title=">>> You received", description=itemListStr)

    return finalEmbed, view


def getItem(itemId: str):
    '''
    Will deepCopy an item so we dont modify the original item by accident
    
    Return : item type object
    '''
    return copy.deepcopy(const.ITEMS_DICT[f'{itemId}'])


def Equipment_Gears_Action(plyer: player.Profile, ctx: discord.ext.commands.Context, isGears: bool, isRemove: bool):
    class DropDownMenu(discord.ui.Select):
        def __init__(self, placeholder: str, plyer: player.Profile, ctx: discord.ext.commands.Context, isGears: bool, isRemove: bool, min_values: int = 1, max_values: int = 1, disabled: bool = False):
            super().__init__(placeholder=placeholder, min_values=min_values,
                             max_values=max_values, disabled=disabled)
            self.player = plyer
            self.ctx = ctx
            self.isGears = isGears
            self.isRemove = isRemove

        async def callback(self, interaction: Interaction):
            print(self.values[0])
            itemName = self.values[0]   # get the choice made
            print(itemName)
            newContent: str = ""
            selectItem: items.Item = None
            for i in const.ITEMS_DICT.values():
                print(i.name)
                if i.simple_name == itemName:
                    selectItem = i
                    # break

            # Actions to make
            if self.isGears:
                if self.isRemove:
                    removeItem = self.player.p_gears.remove(
                        selectItem.armor.type)
                    self.player.inventory.inv.append(removeItem)
                    newContent = f"**{selectItem.name}** has been added to your inventory!"
                else:
                    replaceItem: items.Item = None
                    for i in self.player.inventory.inv:
                        if i.name == selectItem.name:
                            replaceItem = i
                            break
                    removeItem = self.player.p_gears.replace(
                        replaceItem, replaceItem.armor.type)
                    self.player.inventory.inv.remove(replaceItem)
                    newContent = f"**{selectItem.name}** has been added to your gears!"
                    if not removeItem.item_id == items.noneItem.item_id:
                        self.player.inventory.inv.append(removeItem)
                        newContent += f"\n**{removeItem.name}** has been added to your inventory!"
            else:
                if self.isRemove:
                    removeItem = self.player.p_equipment.remove(
                        selectItem.tool.type)
                    self.player.inventory.inv.append(removeItem)
                    newContent = f"**{selectItem.name}** has been added to your inventory!"
                else:
                    replaceItem: items.Item = None
                    for i in self.player.inventory.inv:
                        if i.name == selectItem.name:
                            replaceItem = i
                            break
                    removeItem = self.player.p_equipment.replace(
                        replaceItem, replaceItem.tool.type)
                    self.player.inventory.inv.remove(replaceItem)
                    newContent = f"**{selectItem.name}** has been added to your equipments!"
                    if not removeItem.item_id == items.noneItem.item_id:
                        self.player.inventory.inv.append(removeItem)
                        newContent += f"\n**{removeItem.name}** has been added to your inventory!"

            # /*/**/*/*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*//*//
            self.disabled = True
            await interaction.response.edit_message(content=newContent, view=None)

    view = MyView()
    dropDown = DropDownMenu("nothing yet", plyer=plyer,
                            ctx=ctx, isGears=isGears, isRemove=isRemove)
    listOfChoice = []

    # Make sure the dropdown get the correct info for what action we want to perform
    if isGears:
        if isRemove:
            dropDown.placeholder = "Gear to remove"
            listOfChoice = plyer.getGears()
        else:   # Equip action
            dropDown.placeholder = "Gear to equip"
            listOfChoice = plyer.getGearsInInv()
    else:  # isEquipement then
        if isRemove:
            dropDown.placeholder = "Equipment to remove"
            listOfChoice = plyer.getEquipments()
        else:  # Equip action
            dropDown.placeholder = "Equipment to equip"
            listOfChoice = plyer.getEquipmentInInv()

    # Add the option in the dropdown menu
    # List of values so we dont offer the same item more then once.
    valuesList = []
    for i in listOfChoice:
        if i != f"{items.noneItem.name}" and i.replace(i[0], "") not in valuesList:
            label = i.replace(i[0], "")
            dropDown.add_option(label=label, emoji=i[0])
            valuesList.append(label)

    view.add_item(dropDown)
    return view


# Give out random x nomber of reward in the given list.
def getReward(nb_reward: int, possible_reward: list[items.Item], modifier: list = []):
    '''
    Return the list of rewards that would be given to the player
    '''
    rewards = []
    cpt = 0
    while True:
        if cpt < nb_reward:
            # give a random reward to be given
            reward = choice(possible_reward)

            # TODO apply modifier here

            # add the final reward to the rewards list that will be given to the player
            rewards.append(reward)
        else:
            break
        cpt += 1

    return rewards


# Will give the rewarded experience with all modifier applied if applied
def getXpReward(nb_xp: int, modifier=None):
    '''
    nb_xp : experience number that the player will receive
    Modifier : not done yet
    '''
    # This is just temporary we have'nt done the modifier yet
    return nb_xp


# return a date in a string format
def str_date(date: datetime):
    '''
    return a date in a string format
    '''
    return date.strftime("%m/%d/%Y, %H:%M:%S")


# return a string date to a date object
def strDate_to_date(str_date: str):
    '''
    return a string date to a date object
    '''
    return datetime.strptime(str_date, "%m/%d/%Y, %H:%M:%S")


# the view with all the button for displaying what action the player is curerently ungoing
def getCurrentActionView(as_reward: bool, as_action: bool, player: player.Profile):
    class Modal(discord.ui.Modal):
        def __init__(self, *children: discord.ui.InputText, title: str):
            super().__init__(*children, title=title)
            self.children.append(discord.ui.InputText(style=discord.InputTextStyle.short, label="Are you sure you want to cancel this action?",
                                                      placeholder="yes/no *ONLY*", value="yes", required=True, max_length=3))

        async def callback(self, interaction: Interaction):
            if str.lower(self.children[0].value) == "no":
                await interaction.response.defer()
            elif str.lower(self.children[0].value) == "yes":
                # we reset the player to doing nothing
                player.resetCurrentAction()
                await interaction.response.edit_message(view=getCurrentActionView(False, False, player=player), embed=embeds.getCurrentActionEmbed(
                    ctx=None, action="None", time_until_ready=None, player_name=player.name
                ))
            else:
                await interaction.response.defer()

    class myButton(discord.ui.Button):
        def __init__(self, *, style, label, disabled: bool = False, emoji=None):
            super().__init__(style=style, label=label, disabled=disabled, emoji=emoji)

        async def callback(self, interaction: Interaction):
            match(self.label):
                case "Collect reward":
                    content = ""
                    # All text to send to the player

                    # Items reward text
                    cleanItems = get_cleanItemList(
                        itemList=player.current_Action["rewards"])

                    # Make the check to know if inventory as enough place
                    has_place, slot = check_as_place_inInv(
                        cleanItems, player=player)
                    if has_place:
                        for v1, v2 in cleanItems:   # v1 = item object, v2 = nb of that item
                            # Add the item to the player inevntory
                            itemToInv(player=player, item=v1, nbOfItem=v2)
                            content += f"\n**{v1.name} x{v2}** has been added to your inventory!"

                        # Experience reward text & player receiving their xp rewards
                        for xp_type, xp in player.current_Action.get("xp_rewards"):
                            isLeveling, embed = player.experience.addXp(xp_type=xp_type, amountXp=xp, player_name=player.name)
                            content += f"\nYou have received **{xp}** experience point in **{xp_type}**!"
                            if isLeveling:
                                await interaction.response.send_message(embed=embed)

                        # Send information in the tchat to the player about what he got
                        if not isLeveling:
                            await interaction.response.send_message(content=content, ephemeral=True)
                        else:
                            await interaction.followup.send(content=content, ephemeral=True)

                        # reset the player to doing nothing.
                        player.resetCurrentAction()
                        await interaction.followup.edit_message(message_id=interaction.message.id, view=getCurrentActionView(False, False, player=player),
                                                                embed=embeds.getCurrentActionEmbed(ctx=None, action="None", time_until_ready=None,
                                                                                                   player_name=player.name))
                    else:
                        await interaction.response.send_message(embed=embeds.missingPlaceInInv_Embed(missing_slot=slot), ephemeral=True)
                        await interaction.followup.edit_message(message_id=interaction.message.id, view=view)

                case "Cancel action":
                    await interaction.response.send_modal(Modal(title="Confirm your choice"))
                case _:
                    await interaction.response.defer()

    view = MyView()
    if as_reward or as_action:
        if as_action:
            if as_reward:
                # Check to know if player can receive his reward or is there some time left.
                is_not_finish = True
                if str(get_timeUntilReady(player.current_Action.get("finish_time"))) == "0:00:00:000000":
                    is_not_finish = False

                # Will add the button in both case of above but the button wont be usable if there is some time left to complete the action.
                view.add_item(myButton(style=discord.ButtonStyle.grey,
                                       label="Collect reward", disabled=is_not_finish))
                                       
            # button to cancel action
            view.add_item(
                myButton(style=discord.ButtonStyle.red, label="Cancel action"))

    return view


# get the time left between two datetime object being given. If below zero will return a datetime of 0 days, 0 hour, 0 minutes, 0 seconds
def get_timeUntilReady(readyTime: datetime):
    if readyTime < datetime.now():
        return "0:00:00:000000"
    else:
        return readyTime - datetime.now()


# Receive a list of tuple if u need a list of item but no duplicate and the number of time each item appeir in  the list given
def get_cleanItemList(itemList: list[items.Item]):
    cleanList: list[tuple] = []
    seenItemId = []   # List of item_id that have already been added to the cleanList

    for i in itemList:
        if i.item_id not in seenItemId:
            cleanList.append((i, itemList.count(i)))
            seenItemId.append(i.item_id)

    return cleanList


def skillProgress(current_exp: int, next_levl_exp: int):
    '''
    Return a string with custom emoji to show progression of a skill

    current_exp: int -> current experience of the player in that skill
    next_level_exp: int -> experience needed for the player to level up that skill
    '''

    var1 = int(current_exp / next_levl_exp * 6) # get the number of fill progress bar / 6

    cpt = 0
    text: str = ""
    for x in range(6):
        if cpt < var1:
            text += "<:fillprogress:1046811946046992446>"
        else: 
            text += "<:emptyprogress:1046811849485725836>"
        cpt += 1
    
    return text

###################################################################
# CHECK FUNCTIONS   # DO NOT USE THIS !! PLEASE NOW USE THE FILE FOR CHECKS <3
###################################################################

def check_as_place_inInv(itemList: list[tuple], player: player.Profile):
    '''
    A check to know if all the items that are about the be added to the player inventory can be indeed be added.
    return bool & how many missing slot
    '''
    missing_slot = 0
    for i in itemList:
        if player.inventory.currentInvSize() < player.inventory.inv_size or i[0].simple_name in list(map(lambda x: x.simple_name, player.inventory.inv)):
            pass
        else:
            missing_slot += 1

    if missing_slot > 0:
        return False, missing_slot
    else:
        return True, 0
