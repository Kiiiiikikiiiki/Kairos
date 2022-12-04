import items


class Gears():
    def __init__(self, hat: items.Item = items.noneItem, chestpiece: items.Item = items.noneItem, legspants: items.Item = items.noneItem, gloves: items.Item = items.noneItem,
                 necklace: items.Item = items.noneItem, ring1: items.Item = items.noneItem, ring2: items.Item = items.noneItem):
        self.hat = hat
        self.hatType = "hat"
        self.chestpiece = chestpiece
        self.chestpieceType = "chestpiece"
        self.legspants = legspants
        self.legspantsType = "legspants"
        self.gloves = gloves
        self.glovesType = "gloves"
        self.necklace = necklace
        self.necklaceType = "necklace"
        self.ring1 = ring1
        self.ring2 = ring2
        self.ringType = "ring"

    def replace(self, newGear: items.Item, newGearType: str, ringNumber: int = 1):
        returnGear: items.Item = items.noneItem
        match newGearType:
            case self.hatType:
                returnGear = self.hat
                self.hat = newGear
            case self.chestpieceType:
                returnGear = self.chestpiece
                self.chestpiece = newGear
            case self.legspantsType:
                returnGear = self.legspants
                self.legspants = newGear
            case self.glovesType:
                returnGear = self.gloves
                self.gloves = newGear
            case self.necklaceType:
                returnGear = self.necklace
                self.necklace = newGear
            case self.ringType:
                if ringNumber == 1:
                    returnGear = self.ring1
                    self.ring1 = newGear
                else:
                    returnGear = self.ring2
                    self.ring2 = newGear
            case _:
                print("No matching gear type")
        return returnGear

    def remove(self, gearType: str, ringNumber: int = 1):
        returnGear: items.Item = items.noneItem
        match gearType:
            case self.hatType:
                returnGear = self.hat
                self.hat = items.noneItem
            case self.chestpieceType:
                returnGear = self.chestpiece
                self.chestpiece = items.noneItem
            case self.legspantsType:
                returnGear = self.legspants
                self.legspants = items.noneItem
            case self.glovesType:
                returnGear = self.gloves
                self.gloves = items.noneItem
            case self.necklaceType:
                returnGear = self.necklace
                self.necklace = items.noneItem
            case self.ringType:
                if ringNumber == 1:
                    returnGear = self.ring1
                    self.ring1 = items.noneItem
                else:
                    returnGear = self.ring2
                    self.ring2 = items.noneItem
            case _:
                print("No matching gear type to remove")
        return returnGear
