from discord.ui import Select
from discord import Interaction
from functions import MyView
from interactions import InteractionKairos
from player import Profile
from embeds import locationEmbed
from interactions import testInteractions



class Location:
    def __init__(self, name: str, desc: str, imgLink: str = None, hidden: bool = False, mapId: str = None, type: str = None, coordinate: tuple = None) -> None:
        # Name of the location
        self.name = name
        # Description of the location
        self.desc = desc
        # the map of this location (some location might not have maps tho) Ex: entering a dungeon will just ask you to enter the dongeon but the dongeon will have a map
        self.imgLink = imgLink
        # Does this location is hidden to player without the map for it in their inventory
        self.hidden = hidden
        # An item_id that is needed for the player to have to show this location available
        self.mapId = mapId
        # The type of location -> Ex: Dungeon, Shop, Forge, BountyBoard, etc.
        self.type = type
        # coordinate of the location so we can calculate time of travel
        self.coordinate = coordinate

        self.interaction_list: list[InteractionKairos] = []  # When entering the location this will be the list of possible interaction (object from class Interaction) 


    async def enter(self, player: Profile):
        #TODO when entering, show a dropdown menu with the listed interaction. A picture of the location and things to do 
        # Interactions will be a class with subclass of each possible interaction like talking to this guy, open shop, open forge, etc
        class DropDown(Select):
            def __init__(self, placeholder: str, min_values: int = 1, max_values: int = 1, disabled: bool = False):
                super().__init__(placeholder=placeholder, min_values=min_values, max_values=max_values, disabled=disabled)
            

            async def callback(self, interaction: Interaction):
                pass


        view = MyView() # Make the view
        dropdown = DropDown(placeholder="Choose an interaction") # Create Dropdown select menu

        # Add option to the select menu and make sure player have requirements to access hidden interactions
        for i in self.interaction_list:
            if i.has_requirements is not None or i.has_requirements(player=player):
                dropdown.add_option(label=i.desc)

        # Add dropdown to the view
        view.add_item(dropdown)

        # Making the embed for the location 
        locationEmbed(self.name, self.desc) # TODO add the map of the inside of the location when done making maps

        # Return the view and embed to be showed to the player
        return view, locationEmbed
        


class PointOfInterest:
    def __init__(self, name: str, locationList: list[Location], imgLink: str = None, coordinate: tuple = None):
        self.name = name                # Name of this city
        self.imgLink = imgLink          # the map of this city
        # Locations in the cities (places to go)
        self.locations = locationList
        self.coordinate = coordinate



class Continent:
    def __init__(self, name: str, cityList: list[PointOfInterest], locationList: list[Location], imgLink: str = None, enterLocation: list[Location] = None):
        self.name = name                # Name of the continent
        self.imgLink = imgLink          # the map of this continent
        self.cities = cityList          # All the cities on this continent
        # Those are locations that are not in cities but on continent
        self.locations = locationList
        # Locations that player can enter the continent from
        self.enterLocation = enterLocation




class Maps:
    imgLink: str = None,
    continentList: list[Continent] = None



# =============================================================
# 【Making locations】
# =============================================================

test = Location("Test", "Test description", type="test", coordinate=(10, 40))
test.interaction_list = testInteractions