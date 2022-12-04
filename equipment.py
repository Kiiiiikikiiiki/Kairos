import items


class Equipment():
    def __init__(self, weapon: items.Item = items.noneItem, pickaxe: items.Item = items.noneItem, axe: items.Item = items.noneItem, fishing_rod: items.Item = items.noneItem,
                 scythe: items.Item = items.noneItem, knife: items.Item = items.noneItem, lockpick: items.Item = items.noneItem, forge_hammer: items.Item = items.noneItem):
        self.weapon = weapon
        self.weaponType = "weapon"
        self.pickaxe = pickaxe
        self.pickaxeType = "pickaxe"
        self.axe = axe
        self.axeType = "axe"
        self.fishing_rod = fishing_rod
        self.fishing_rodType = "fishing_rod"
        self.scythe = scythe
        self.scytheType = "scythe"
        self.knife = knife
        self.knifeType = "knife"
        self.lockpick = lockpick
        self.lockpickType = "lockpick"
        self.forge_hammer = forge_hammer
        self.forge_hammerType = "forge_hammer"

    def replace(self, newEquipment: items.Item, newEquipmentType: str):
        returnEquipment: items.Item = items.noneItem
        match newEquipmentType:
            case self.weaponType:
                returnEquipment = self.weapon
                self.weapon = newEquipment
            case self.pickaxeType:
                returnEquipment = self.pickaxe
                self.pickaxe = newEquipment
            case self.axeType:
                returnEquipment = self.axe
                self.axe = newEquipment
            case self.fishing_rodType:
                returnEquipment = self.fishing_rod
                self.fishing_rod = newEquipment
            case self.scytheType:
                returnEquipment = self.scythe
                self.scythe = newEquipment
            case self.knifeType:
                returnEquipment = self.knife
                self.knife = newEquipment
            case self.lockpickType:
                returnEquipment = self.lockpick
                self.lockpick = newEquipment
            case self.forge_hammerType:
                returnEquipment = self.forge_hammer
                self.forge_hammer = newEquipment
            case _:
                print("No matching equipment type")
        return returnEquipment

    def remove(self, equipmentType: str):
        returnEquipment: items.Item = items.noneItem
        match equipmentType:
            case self.weaponType:
                returnEquipment = self.weapon
                self.weapon = items.noneItem
            case self.pickaxeType:
                returnEquipment = self.pickaxe
                self.pickaxe = items.noneItem
            case self.axeType:
                returnEquipment = self.axe
                self.axe = items.noneItem
            case self.fishing_rodType:
                returnEquipment = self.fishing_rod
                self.fishing_rod = items.noneItem
            case self.scytheType:
                returnEquipment = self.scythe
                self.scythe = items.noneItem
            case self.knifeType:
                returnEquipment = self.knife
                self.knife = items.noneItem
            case self.lockpickType:
                returnEquipment = self.lockpick
                self.lockpick = items.noneItem
            case self.forge_hammerType:
                returnEquipment = self.forge_hammer
                self.forge_hammer = items.noneItem
            case _:
                print("No matching equipment type")
        return returnEquipment
