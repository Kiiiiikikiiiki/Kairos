from items import Item


class Inventory:
    def __init__(self, inv: list[Item] = [], inv_size: int = 30):
        self.inv = inv
        self.inv_size = inv_size

    def currentInvSize(self):
        '''
        Know to current size of the player inventory (how mamy slots)
        '''
        # List of item without duplicate to know how many slot the player is using
        noDuplicateInv = []
        for i in self.inv:
            if i.simple_name not in noDuplicateInv:
                noDuplicateInv.append(i.simple_name)
        return len(noDuplicateInv)
