from locationType import LocationType


class Location:
    def __init__(self, name: str, imgLink: str = None, hidden: bool = False, mapId: str = None, type: LocationType = None, coordinate: tuple = None) -> None:
        self.name = name
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
