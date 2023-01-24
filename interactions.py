import items

class Shop:
    def __init__(self, buying_items: list[items.Item], selling_items: list[tuple], trading_items: list[tuple]):
        pass

    def interact(self, **kwargs):
        pass


class Interaction:
    def __init__(self, description: str, subInteraction: any):
        '''
        description: Short description of the interaction to show in a dropdown
        subInteraction: The interaction type (ex: shop, talking and forge) so we can interact with the correct interaction
        '''
        self.desc = description
        self.subInteraction = subInteraction
    

    def interact(self, **kwargs):
        return self.subInteraction.interact(kwargs)