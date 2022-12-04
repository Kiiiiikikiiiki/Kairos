import json
from datetime import datetime
import profile
import player
import guild
import inventory
import items
import pockethouse
import xp
import incubator
import gears
import equipment
import constant as const
import copy
from functions import str_date, strDate_to_date


# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /*/*/*/*/*/*/ SERIALIZATION /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
def save_profile(profiles_list: list[player.Profile]):
    with open("db/profiles.txt", 'r') as f:
        profiles_dict = json.load(f)    # Get the oldest data dict
        for profile in profiles_list:
            profiles_dict[f'{profile.profile_id}'] = {
                'name': profile.name,
                'money': profile.money,
                'guild': profile.guild,
                'location': profile.location,
                'active_quest': profile.active_quest,
                'requirement': profile.requirement
            }
    with open("db/profiles.txt", 'w') as f:
        json.dump(profiles_dict, f, indent=4)

    save_inventory(profiles_list=profiles_list)
    save_xp(profiles_list=profiles_list)
    save_gears(profiles_list=profiles_list)
    save_equipment(profile_list=profiles_list)
    save_currentAction(profile_list=profiles_list)
    return True


def save_inventory(profiles_list: list[player.Profile]):
    with open("db/inventory.txt", 'r') as f:
        inv_dict = json.load(f)    # Get the oldest data dict
        for profile in profiles_list:

            inv = getListOfItemToSave(profile.inventory.inv)

            inv_dict[f'{profile.profile_id}'] = {
                "inv_size": profile.inventory.inv_size,
                "inv": inv
            }
    with open("db/inventory.txt", 'w') as f:
        json.dump(inv_dict, f, indent=4)
    return True


def save_xp(profiles_list: list[player.Profile]):
    with open("db/xp.txt", 'r') as f:
        xp_dict = json.load(f)  # Get the oldest data dict
        for profile in profiles_list:
            xp_dict[f'{profile.profile_id}'] = profile.experience.skills
    with open("db/xp.txt", 'w') as f:
        json.dump(xp_dict, f, indent=4)
    return True


def save_guild(guild_list: list[guild.guild]):
    with open("db/guild.txt", 'r') as f:
        guild_dict = json.load(f)   # Get the oldest data dict
        for guild in guild_list:
            guild_dict[f'{guild.name}'] = {
                'name': guild.name,
                'color': guild.color,
                'bank_money': guild.bank_money,
                'private': guild.private,
                'members_rank': guild.members_rank
            }
    with open("db/guild.txt", 'w') as f:
        json.dump(guild_dict, f, indent=4)
    return True


def save_phouse(profiles_list: list[player.Profile]):
    with open("db/pockethouse.txt", 'r') as f:
        phouse_dict = json.load(f)  # Get the oldest data dict
        for profile in profiles_list:
            # Incubators saves
            incubator_list: list = []
            for i in profile.pockethouse.incubators:
                if i.active_egg:
                    str_timeEggReady = i.timeEggReady.strftime(
                        "%m/%d/%Y, %H:%M:%S")    # Convert datetime object to string
                    incubator_list.append(
                        {
                            'egg': {'item_id': i.egg.item_id, 'condition': i.egg.condition},
                            'active_egg': i.active_egg,
                            'timeEggReady': str_timeEggReady
                        }
                    )
                else:
                    incubator_list.append(
                        {
                            'active_egg': i.active_egg
                        }
                    )
            # pHouse
            phouse_dict[f'{profile.profile_id}'] = {
                'upgrade': profile.pockethouse.upgrade,
                'workbench': profile.pockethouse.workbench,
                'cookingStation': profile.pockethouse.cookingStation,
                'alchemyStation': profile.pockethouse.alchemyStation,
                'forge': profile.pockethouse.forge,
                'eggIncubator': profile.pockethouse.eggIncubator,
                'incubators': incubator_list,
                'mapReader': profile.pockethouse.mapReader,
                'enchantingPool': profile.pockethouse.enchantingPool
            }
    with open("db/pockethouse.txt", 'w') as f:
        json.dump(phouse_dict, f, indent=4)

    save_phouse_storage(profiles_list=profiles_list)
    return True


def save_phouse_storage(profiles_list: list[player.Profile]):
    with open("db/pockethouseStorage.txt", 'r') as f:
        phouseInv_dict = json.load(f)   # Get the oldest data dict
        for profile in profiles_list:
            inv = getListOfItemToSave(profile.pockethouse.storage)
            phouseInv_dict[f'{profile.profile_id}'] = {
                "storage_size": profile.pockethouse.storage_size,
                "storage": inv
            }
    with open("db/pockethouseStorage.txt", 'w') as f:
        json.dump(phouseInv_dict, f, indent=4)
    return True


# not tested
def save_gears(profiles_list: list[player.Profile]):
    with open("db/gears.txt", 'r') as f:
        gearsDict = json.load(f)    # Get the oldest data dict
        for profile in profiles_list:
            profileGearsDict = {}

            hat = profile.p_gears.hat
            profileGearsDict["hat"] = {
                "itemId": hat.item_id, "condition": hat.condition}

            chestpiece = profile.p_gears.chestpiece
            profileGearsDict["chestpiece"] = {
                "itemId": chestpiece.item_id, "condition": chestpiece.condition}

            legspants = profile.p_gears.legspants
            profileGearsDict["legspants"] = {
                "itemId": legspants.item_id, "condition": legspants.condition}

            gloves = profile.p_gears.gloves
            profileGearsDict["gloves"] = {
                "itemId": gloves.item_id, "condition": gloves.condition}

            necklace = profile.p_gears.necklace
            profileGearsDict["necklace"] = {
                "itemId": necklace.item_id, "condition": necklace.condition}

            ring1 = profile.p_gears.ring1
            profileGearsDict["ring1"] = {
                "itemId": ring1.item_id, "condition": ring1.condition}

            ring2 = profile.p_gears.ring2
            profileGearsDict["ring2"] = {
                "itemId": ring2.item_id, "condition": ring2.condition}

            gearsDict[f"{profile.profile_id}"] = profileGearsDict
    with open("db/gears.txt", 'w') as f:
        json.dump(gearsDict, f, indent=4)
    return True


# not tested
def save_equipment(profile_list: list[player.Profile]):
    with open("db/equipment.txt", 'r') as f:
        equipmentDict = json.load(f)    # Get the oldest data dict
        for profile in profile_list:
            profileEquipDict = {}

            weapon = profile.p_equipment.weapon
            profileEquipDict["weapon"] = {
                "itemId": weapon.item_id, "condition": weapon.condition}

            pickaxe = profile.p_equipment.pickaxe
            profileEquipDict["pickaxe"] = {
                "itemId": pickaxe.item_id, "condition": pickaxe.condition}

            axe = profile.p_equipment.axe
            profileEquipDict["axe"] = {
                "itemId": axe.item_id, "condition": axe.condition}

            fishing_rod = profile.p_equipment.fishing_rod
            profileEquipDict["fishing_rod"] = {
                "itemId": fishing_rod.item_id, "condition": fishing_rod.condition}

            scythe = profile.p_equipment.scythe
            profileEquipDict["scythe"] = {
                "itemId": scythe.item_id, "condition": scythe.condition}

            knife = profile.p_equipment.knife
            profileEquipDict["knife"] = {
                "itemId": knife.item_id, "condition": knife.condition}

            lockpick = profile.p_equipment.lockpick
            profileEquipDict["lockpick"] = {
                "itemId": lockpick.item_id, "condition": lockpick.condition}

            forge_hammer = profile.p_equipment.forge_hammer
            profileEquipDict["forge_hammer"] = {
                "itemId": forge_hammer.item_id, "condition": forge_hammer.condition}

            equipmentDict[f"{profile.profile_id}"] = profileEquipDict

    with open("db/equipment.txt", 'w') as f:
        json.dump(equipmentDict, f, indent=4)
    return True


# not tested
def save_currentAction(profile_list: list[player.Profile]):
    with open("db/currentAction.txt", "r") as f:
        currentAction_dict = json.load(f)

        for profile in profile_list:
            # If not None will transform the date object to a tring that can be save in json
            finish_time = profile.current_Action["finish_time"]
            if profile.current_Action["finish_time"] is not None:
                print("is not none")
                finish_time = str_date(finish_time)
            else:
                print("is none")
                finish_time = "None"

            # Make all the rewards into a dict that can be save in json
            rewards = profile.current_Action["rewards"]
            if profile.current_Action["rewards"] is not None:
                rewards = getListOfItemToSave(
                    profile.current_Action["rewards"])
            else:
                rewards = "None"

            currentAction_dict[f"{profile.profile_id}"] = {
                "action": profile.current_Action["action"],
                "finish_time": finish_time,
                "rewards": rewards,
                "xp_rewards": profile.current_Action["xp_rewards"]
            }
    with open("db/currentAction.txt", "w") as f:
        json.dump(currentAction_dict, f, indent=4)
    return True


def getListOfItemToSave(items_list: list[items.Item]):
    '''
    Will return a list of -Object Item- in a dict so it can be stored in a json files
    '''
    inv = []
    seenItem = []
    itemsTuple = list(map(lambda x: (x.item_id, x.condition), items_list))
    for i in items_list:
        if (i.item_id, i.condition) not in seenItem:
            inv.append({
                'item_id': i.item_id,
                'condition': i.condition,
                'nb': itemsTuple.count((i.item_id, i.condition))
            })
            seenItem.append((i.item_id, i.condition))
    return inv


# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /*/*/*/*/*/*/ DESERIALIZATION /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
def jsonItemsTo_object(listOfItems: list[dict]):
    object_list: list[items.Item] = []

    for i in listOfItems:
        i_id = i["item_id"]                                 # Get item id
        # Get the item object related to that id
        base_item: items.Item = const.ITEMS_DICT[f"{i_id}"]
        # Create new instance of that base item so we dont modify the model item
        item = copy.deepcopy(base_item)
        item.condition = i["condition"]
        for r in range(i['nb']):
            object_list.append(item)
    return object_list


def jsonItemTo_object(itemId: str, condition: str):
    # Get the item object related to that id
    base_item: items.Item = const.ITEMS_DICT[f"{itemId}"]
    # Create new instance of that base item so we dont modify the model item
    item = copy.deepcopy(base_item)
    item.condition = condition

    return item


def deserialize_profile():
    with open("db/profiles.txt", 'r') as f:
        profiles_dict = json.load(f)
        for p_id, p_info in profiles_dict.items():
            profile_id = p_id
            profile_name = p_info["name"]
            profile_money = p_info["money"]
            profile_guild = p_info["guild"]
            profile_location = p_info["location"]
            profile_active_quest = p_info["active_quest"]
            profile_requirement = p_info["requirement"]
            new_profile = player.Profile(profile_name, profile_id, money=profile_money, guild=profile_guild, location=profile_location,
                                         inventory=deserialize_inventory(
                                             profile_id),
                                         experience=deserialize_xp(profile_id),
                                         pockethouse=deserialize_phouse(
                                             profile_id),
                                         p_gears=deserialize_gears(profile_id),
                                         p_equipment=deserialize_equipment(
                                             profile_id),
                                         current_Action=deserialize_currentAction(profile_id))
            new_profile.active_quest = profile_active_quest
            new_profile.requirement = profile_requirement
            const.PROFILE_DICT[f'{profile_id}'] = new_profile


def deserialize_inventory(profile_id: str):
    with open("db/inventory.txt", 'r') as f:
        inv_dict = json.load(f)    # Get the oldest data dict
        # Get inventory for the selected player
        profile_inv_dict = inv_dict.get(profile_id)
        new_inv = inventory.Inventory()
        new_inv.inv_size = profile_inv_dict["inv_size"]
        new_inv.inv = jsonItemsTo_object(profile_inv_dict["inv"])
    return new_inv


def deserialize_gears(profile_id: str):
    with open("db/gears.txt", 'r') as f:
        gearsDict = json.load(f)
        # Get gears for the selected player
        profileGears = gearsDict.get(profile_id)
        new_gears = gears.Gears()
        # Assigning the gears
        new_gears.hat = jsonItemTo_object(
            itemId=profileGears["hat"]["itemId"], condition=profileGears["hat"]["condition"])
        new_gears.chestpiece = jsonItemTo_object(
            itemId=profileGears["chestpiece"]["itemId"], condition=profileGears["chestpiece"]["condition"])
        new_gears.legspants = jsonItemTo_object(
            itemId=profileGears["legspants"]["itemId"], condition=profileGears["legspants"]["condition"])
        new_gears.gloves = jsonItemTo_object(
            itemId=profileGears["gloves"]["itemId"], condition=profileGears["gloves"]["condition"])
        new_gears.necklace = jsonItemTo_object(
            itemId=profileGears["necklace"]["itemId"], condition=profileGears["necklace"]["condition"])
        new_gears.ring1 = jsonItemTo_object(
            itemId=profileGears["ring1"]["itemId"], condition=profileGears["ring1"]["condition"])
        new_gears.ring2 = jsonItemTo_object(
            itemId=profileGears["ring2"]["itemId"], condition=profileGears["ring2"]["condition"])

        return new_gears


def deserialize_equipment(profile_id: str):
    with open("db/equipment.txt", "r") as f:
        equipDict = json.load(f)
        # Get equipments for the selected player
        profileEquipment = equipDict.get(profile_id)
        new_equipment = equipment.Equipment()
        # Assigning the equipment
        new_equipment.weapon = jsonItemTo_object(
            itemId=profileEquipment["weapon"]["itemId"], condition=profileEquipment["weapon"]["condition"])
        new_equipment.pickaxe = jsonItemTo_object(
            itemId=profileEquipment["pickaxe"]["itemId"], condition=profileEquipment["pickaxe"]["condition"])
        new_equipment.axe = jsonItemTo_object(
            itemId=profileEquipment["axe"]["itemId"], condition=profileEquipment["axe"]["condition"])
        new_equipment.fishing_rod = jsonItemTo_object(
            itemId=profileEquipment["fishing_rod"]["itemId"], condition=profileEquipment["fishing_rod"]["condition"])
        new_equipment.scythe = jsonItemTo_object(
            itemId=profileEquipment["scythe"]["itemId"], condition=profileEquipment["scythe"]["condition"])
        new_equipment.knife = jsonItemTo_object(
            itemId=profileEquipment["knife"]["itemId"], condition=profileEquipment["knife"]["condition"])
        new_equipment.lockpick = jsonItemTo_object(
            itemId=profileEquipment["lockpick"]["itemId"], condition=profileEquipment["lockpick"]["condition"])
        new_equipment.forge_hammer = jsonItemTo_object(
            itemId=profileEquipment["forge_hammer"]["itemId"], condition=profileEquipment["forge_hammer"]["condition"])

        return new_equipment


# Not tested
def deserialize_currentAction(profile_id: str):
    with open("db/currentAction.txt", "r") as f:
        currentAction_dict = json.load(f)
        profile_currentAction = currentAction_dict.get(profile_id)

        # Make sure finish_time is not none to convert it
        finish_time = profile_currentAction["finish_time"]
        if finish_time != "None":
            finish_time = strDate_to_date(finish_time)
        else:
            finish_time = None

        # Make sure rewards is not none to convert it
        rewards = profile_currentAction["rewards"]
        if rewards != "None":
            rewards = jsonItemsTo_object(rewards)
        else:
            rewards = None

        currentAction = {}
        currentAction["action"] = profile_currentAction["action"]
        currentAction["finish_time"] = finish_time
        currentAction["rewards"] = rewards
        currentAction["xp_rewards"] = profile_currentAction["xp_rewards"]

        return currentAction


def deserialize_xp(profile_id: str):
    with open("db/xp.txt", 'r') as f:
        xp_dict = json.load(f)
        # Get xp for the selected player
        profile_xp_dict = xp_dict.get(profile_id)
        new_xp = xp.exp()
        if profile_xp_dict != None:
            new_xp.skills = profile_xp_dict
    return new_xp


def deserialize_guild():
    pass


def deserialize_phouse(profile_id: str):
    with open("db/pockethouse.txt", 'r') as f:
        phouse_dict = json.load(f)  # Get the oldest data dict
        # Get phouse for the selected player
        profile_phouse_dict = phouse_dict.get(profile_id)
        new_phouse = pockethouse.P_house()
        new_phouse.upgrade = profile_phouse_dict["upgrade"]
        new_phouse.workbench = profile_phouse_dict["workbench"]
        new_phouse.cookingStation = profile_phouse_dict["cookingStation"]
        new_phouse.alchemyStation = profile_phouse_dict["alchemyStation"]
        new_phouse.forge = profile_phouse_dict["forge"]
        new_phouse.eggIncubator = profile_phouse_dict["eggIncubator"]
        new_phouse.mapReader = profile_phouse_dict["mapReader"]
        new_phouse.enchantingPool = profile_phouse_dict["enchantingPool"]
        new_phouse.storage, new_phouse.storage_size = deserialize_phouse_storage(
            profile_id)

        # Incubator section
        incubators: list[incubator.Incubator] = []
        incubators_list = profile_phouse_dict["incubators"]
        for inc in incubators_list:
            new_incubator = incubator.Incubator()
            if inc["active_egg"]:
                new_incubator.active_egg = True

                # Get item id
                i_id = inc["egg"]["item_id"]
                # Get the item object related to that id
                base_item: items.Item = const.ITEMS_DICT[f"{i_id}"]
                # Create new instance of that base item so we dont modify the model item
                item = copy.deepcopy(base_item)
                item.condition = inc["egg"]["condition"]
                new_incubator.egg = item
                new_incubator.timeEggReady = datetime.strptime(
                    inc["timeEggReady"], "%m/%d/%Y, %H:%M:%S")
            incubators.append(new_incubator)

        new_phouse.incubators = incubators
    return new_phouse


def deserialize_phouse_storage(profile_id: str):
    with open("db/pockethouseStorage.txt", 'r') as f:
        storage_dict = json.load(f)    # Get the oldest data dict
        # Get storage for the selected player
        phouse_storage_dict = storage_dict.get(profile_id)
        new_storage: list[items.Item] = []
        storage_size = phouse_storage_dict["storage_size"]
        new_storage = jsonItemsTo_object(phouse_storage_dict["storage"])
    return new_storage, storage_size
