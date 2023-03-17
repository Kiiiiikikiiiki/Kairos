class Weapon:
    def __init__(self, p_damage: float=0, e_damage: float=0, edition: str = 'Basic'):
        self.p_damage = p_damage            # physical damage
        self.e_damage = e_damage            # elemental damage
        self.edition = edition


class Pickaxe:
    def __init__(self, strength: int, durability: int):
        self.strength = strength
        self.durability = durability
        self.broken = False


class Fishing_Rod:
    def __init__(self, durability: int):
        self.durability = durability


class Armor:
    def __init__(self, type: str, p_defence: float=0, e_defence: float=0, bonus_health: float=0,
                 edition: str = 'Basic'):
        # Type of the armor -> Ex : hat, chestpiece, legspants, gloves, etc.
        self.type = type
        self.p_defence = p_defence          # physical defence
        self.e_defence = e_defence          # elemental defence
        self.bonus_health = bonus_health
        self.edition = edition


class Key:
    def __init__(self, open: str = "", ):
        self.open = open


class Crate:
    def __init__(self, item_list: list, name: str = "", config: dict = None, info: str = ""):
        self.name = name
        self.item_list = item_list
        self.config = config
        self.info = info

        self.desc = ''
        for i in item_list:
            self.desc += f'{i.name}\n'


class Tool:
    def __init__(self, type: str, wepaon: Weapon = None, pickaxe: Pickaxe = None, fishing_rod: Fishing_Rod = None):
        # Type of the tool -> Ex: weapon, pickaxe, axe, knife, fishing_rod, etc.
        self.type = type

        self.weapon = wepaon
        self.pickaxe = pickaxe
        self.fishing_rod = fishing_rod


class Rock:
    def __init__(self, toughness):
        self.toughness = toughness


class Item:
    def __init__(self, item_id: str, name: str, simple_name: str, rarity: str, desc: str, usable: bool = False,
                 condition: str = 'Perfect', can_sell: bool = False, resell_value: float = 0, is_armor: bool = False,
                 is_key: bool = False, is_crate: bool = False, is_tool: bool = False, armor: Armor = None,
                 key: Key = None, crate: Crate = None, tool: Tool = None):
        self.item_id = item_id
        self.name = name
        self.simple_name = simple_name  # the name without the pic of the item
        self.rarity = rarity
        self.desc = desc                # "Description"
        self.usable = usable            # If the item can be used by func use()
        # Condition of the item : ( Perfect, Dusty, Damaged, Broken)
        self.condition = condition
        self.can_sell = can_sell
        self.resell_value = resell_value

        self.is_armor = is_armor         # identifier to categories the item
        self.is_key = is_key            # identifier to categories the item
        self.is_crate = is_crate        # identifier to categories the item
        self.is_tool = is_tool          # identifier to categories the item

        self.armor = armor
        self.key = key
        self.crate = crate
        self.tool = tool

    
    def __eq__(self, __o: object) -> bool:  #TODO test
        if self.__class__ is __o.__class__:
            return (self.item_id, self.condition) == (__o.item_id, __o.condition)
        else:
            return NotImplemented


    def display(self, nbOfItem: int = 0):
        url = "https://www.google.com/"
        if nbOfItem == 0:
            return f"[`{self.name}`]({url} '{self.desc}')"
        else:
            return f"[`{self.name} [{nbOfItem}]`]({url} '{self.desc}')"


# /*/*/*/*/*/*/*/ ITEMS /*/*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
noneItem = Item("0000", "❌None", "none", "none", "")
test1 = Item("0001", "🍎Apple", "test1", "Commun",
             "Just a nice 🍎Apple for you to eat", usable=True)
test2 = Item("0002", "🧪Potion of heal", "test2", "commun",
             "❤Heal for 10% of your max health", usable=True)
test3 = Item("0003", "🔰Shield of light", "test3", "commun",
             "Add 100 physical defence to your character when equiped")
armor_test4 = Armor("hat")
test4 = Item("0004", "🎩Hat of the tester", "Hat of the tester", "commun",
             "this 🎩hat does nothing..", is_armor=True, armor=armor_test4)
test5 = Item("0005", "🎩Veagan hat", "Veagan hat", "commun",
             "MASTER OF THEM ALL", is_armor=True, armor=armor_test4)
test6 = Item("0006", "🗡Daggerite", "Daggerite", "commun",
             "🗡Daggerite is no use but yeah sure it look kinda cool", is_tool=True, tool=Tool("weapon", wepaon=Weapon()))
test7 = Item("0007", "🗡Sword Of Hope", "Sword Of Hope", "commun",
             "🗡Sword Of Hope is nothing but hope for this game", is_tool=True, tool=Tool("weapon", wepaon=Weapon()))
test8 = Item("0008", "💎Ruby", "Ruby", "commun", "Precious stone")
test9 = Item("0009", "💎Diamond", "Diamond", "commun", "Precious stone")
test10 = Item("0010", "⛏Iron Pickaxe", "Iron Pickaxe", "commun",
              "Just a basic pickaxe", is_tool=True, tool=Tool("pickaxe", pickaxe=Pickaxe(1, 1)))
test11 = Item("0011", "🪨Stone", "Stone", "commun", "Basic material")
test12 = Item("0012", "⛏Elden Pickaxe", "Elden Pickaxe", "mystic",
              "Pickaxe that was use by the ancient dwarf civilization", is_tool=True, tool=Tool("pickaxe", pickaxe=Pickaxe(5, 20)))
test13 = Item("0013", "Star Fish", "Star Fish",
              "rare", "A rare test fish i guess")
test14 = Item("0014", "Shark", "Shark", "rare", "Scarryyy sharkk:)")
test15 = Item("0015", "Salmon", "Salmon", "commun",
              "Im giving up on description at this point..")
test16 = Item("0016", "🎣Basic Rod", "Basic Rod", "commun", "Just throw it and see <3",
              is_tool=True, tool=Tool("fishing_rod", fishing_rod=Fishing_Rod(5)))
