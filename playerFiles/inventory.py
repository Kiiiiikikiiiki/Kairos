from items import Item


class Inventory:
    def __init__(self, inv: list[dict], inv_size: int = 30):
        self.inv = inv
        self.inv_size = inv_size


    def add_items(self, items: list[dict], player: any):
        '''
        Add item(s) to the current inventory
        The list must contain dicts that are formated that way : 
            {'item': itemObject,
             'nb': number of the item that is being added to the inventory}

        Parameters
        ----------
        items : list[dict{'item': Item, 'nb': Number of that item}]
        player : Profile class object
            Is set to any to avoid circular import in the inventory file
        '''
        added = False
        for item in items:
            for i in self.inv:
                if i['item'].condition == item['item'].condition and i['item'].item_id == item['item'].item_id:   # Check if the item is identical 
                    # If identical
                    i['nb'] += item['nb']  # Add the number of that item that needed to be added to the inventory
                    added = True
                    break
            if not added:
                self.inv.append({
                    'item': item['item'],
                    'nb': item['nb']
                })

        # Save inventory
        from newDB.database_func import saveInventory
        saveInventory(profile=player)


    def remove_items(self, items: list[dict], player: any):
        '''
        Remove item(s) from the current inventory
        The list must contain dicts that are formated that way : 
            {'item': itemObject,
             'nb': number of the item that is being remove to the inventory}

        Parameters
        ----------
        items: list[dict{'item': Item, 'nb': Number of that item}]
        player : Profile class object
            Is set to any to avoid circular import in the inventory file
        '''
        for item in items:
            index = self.find_item(item['item']) # Find where the item is in the inventory
            if index is not None:
                remaining = self.inv[index]['nb'] - item['nb'] # Get the remaining of the item and if 0 will completly delete the item from inventory
                if remaining == 0:
                    self.inv.pop(index)
                else:
                    self.inv[index]['nb'] = remaining
        
        # Save inventory
        from newDB.database_func import saveInventory
        saveInventory(profile=player)
            


    def check_item(self, item: Item, nb):
        '''
        Check if the item is in the inventory and if the required amount is met too. 
        item: Item object 
        nb: Number of that item that must be in the inventory

        return True if the item is in the inventory and if it has the required amount of that item
        '''
        
        # Make a new list with only the corresponding item
        new_list = [i for i in self.inv if i['item'].item_id == item.item_id and i['item'].condition == item.condition]
        if len(new_list) != 0:
            # Check if the inventory contain the requested amount of the item
            if new_list[0]['nb'] >= nb:
                return True
        return False


    def find_item(self, item: Item):
        '''
        Will find the item in the inventory and return the index of the item in the inventory
        
        item: Item object 

        Return: The index (None if False)
        '''

        for i in self.inv:
            if i['item'].item_id == item.item_id and i['item'].condition == item.condition:
                return self.inv.index(i)
        return None

    
    def nbItem(self, item: Item):
        '''
        Will tell how many of that item is present in the inventory

        Return number of that item object
        '''
        pass