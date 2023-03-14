from items import Item


class Inventory:
    def __init__(self, inv: list[tuple], inv_size: int = 30):
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


    def add_items(self, items: list[tuple]):
        '''
        Add item(s) to the current inventory
        The list must contain tuple of an item and the number of that item that is being added 
        '''
        added = False
        for item, nb in items:
            for i in self.inv:
                if i[0].condition == item.condition and i[0].item_id == item.item_id:   # Check if the item is identical 
                    # If identical
                    i[1] += nb  # Add the number of that item that needed to be added to the inventory
                    added = True
                    break
            if not added:
                self.inv.append((item, nb))


    def remove_items(self, items: list[tuple]):
        '''
        Remove item(s) from the current inventory
        The list must contain tuple of an item and the number of that item that is being removed
        '''
        pass


    def check_item(self, item: Item, nb):
        '''
        Check if the item is in the inventory and if the required amount is met too. 
        item: Item object 
        nb: Number of thta item that must be in the inventory
        '''
        pass