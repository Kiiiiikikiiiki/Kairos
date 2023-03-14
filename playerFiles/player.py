import pockethouse as ph
import playerFiles.inventory as inv
import playerFiles.xp as xp
import playerFiles.gears as gears
import playerFiles.equipment as equipment
from datetime import datetime
import functions


class Profile:
    def __init__(self, name: str, profile_id: str, pockethouse: ph.P_house = ph.P_house(), inventory: inv.Inventory = inv.Inventory([]), p_gears: gears.Gears = gears.Gears(),
                 p_equipment: equipment.Equipment = equipment.Equipment(),
                 money: float = 0, experience: xp.exp = xp.exp(), guild: str = "Solo-Player", location: str = "EtherCity",
                 current_Action: dict = {"action": "None", "finish_time": None, "rewards": None, "xp_rewards": []}):

        # list of quest_id so bot can detect wich quest is active for each player
        self.active_quest: list = []

        # After an event that is either a obtainable requirement or not it will go there
        self.requirement: list = []

        self.name = name                        # Name of player :)
        self.profile_id = profile_id            # Simple Player ID
        # A place the player can go while staying at is location where he can do a lot of stuff
        self.pockethouse = pockethouse
        self.inventory = inventory              # Little or big storage place..
        self.p_gears = p_gears                  # All the gears of the player
        # All equipment like weapon and tools of the player
        self.p_equipment = p_equipment
        self.money = money                      # $$$$
        # take care of all lvl or exp related to the player
        self.experience = experience
        self.guild = guild                      # If u have friend you have a guild <3
        # Current localisation of a player on the map
        self.location = location
        # The action the player is currently doing that prevent him from doing something else
        self.current_Action = current_Action

    def getGearsInInv(self):
        '''
        Return a list of gears name that the player has in is inventory
        '''
        gearsList: list[str] = []
        for i in self.inventory.inv:
            if i.is_armor:
                gearsList.append(i.name)
        return gearsList

    def getGears(self):
        '''
        Return a list of name of the gears the player has equip on him
        '''
        gearsList: list[str] = [
            self.p_gears.hat.name,
            self.p_gears.chestpiece.name,
            self.p_gears.legspants.name,
            self.p_gears.gloves.name,
            self.p_gears.necklace.name,
            self.p_gears.ring1.name,
            self.p_gears.ring2.name
        ]
        return gearsList

    def getEquipments(self):
        '''
        Return a list of name of the gears the player has equip on him
        '''
        equipmentsList: list[str] = [
            self.p_equipment.weapon.name,
            self.p_equipment.pickaxe.name,
            self.p_equipment.axe.name,
            self.p_equipment.fishing_rod.name,
            self.p_equipment.scythe.name,
            self.p_equipment.knife.name,
            self.p_equipment.lockpick.name,
            self.p_equipment.forge_hammer.name
        ]
        return equipmentsList

    def getEquipmentInInv(self):
        '''
        Return a list of equipment name that the player has in is inventory
        '''
        equipmentsList: list[str] = []
        for i in self.inventory.inv:
            if i.is_tool:
                equipmentsList.append(i.name)
        return equipmentsList

    def resetCurrentAction(self):
        '''
        reset the player at doing nothing.
        '''
        self.current_Action = {
            "action": "None",
            "finish_time": None,
            "rewards": None,
            "xp_rewards": []
        }

    def is_action_done(self):
        '''
        Check if the player has done is time to finish is action and if he doesnt have a reward
        to collect then we will automaticly reset is current action to doing nothing.

        return True if action has been reset if not than return False
        '''

        # Make the check and reset player current action if all condition are filled
        if self.current_Action.get("rewards") is None and functions.get_timeUntilReady(self.current_Action.get("finish_time")) == "0:00:00:000000":
            self.resetCurrentAction()
            return True

        return False 
