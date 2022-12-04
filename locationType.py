class Shop:
    def __init__(self, name: str):
        self.name = name
    

    def display(self, **kwargs):
        pass


class LocationType:
    def __init__(self, type: any):
        self.type = type # Class from locationType 
    

    def display(self, **kwargs):
        return self.type.display(kwargs)