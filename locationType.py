import items

class Shop:
    def __init__(self, buying_items: list[items.Item], selling_items: list[tuple], trading_items: list[tuple]):
        pass

    def display(self, **kwargs):
        pass


class LocationType:
    def __init__(self, type: any):
        self.type = type # Class from locationType 
    

    def display(self, **kwargs):
        return self.type.display(kwargs)