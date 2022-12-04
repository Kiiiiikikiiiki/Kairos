import items
import mailbox
import incubator


class P_house:
    def __init__(self):

        # House can upgrade and unlock new things this is to know what upgrade your at
        self.upgrade: int = 0

        # /*/*/*/*/*/ All the upgrade below are subject to change and only work in progress /*/*/*//*/**/*//*/
        # Upgrade 0:
        # You have an other inventory
        self.storage: list[items.Item] = []
        self.storage_size = 10
        # Mailbox (Receive mail items -> messages, items, quests, etc)
        self.mailbox: mailbox.Mailbox = mailbox.Mailbox()
        # Upgrade 1:
        # - Unlock Workbench (not implemented)
        self.workbench = False
        # Upgrade 2:
        # - Cooking station (not implemented)
        self.cookingStation = False
        # - Alchemy Station (not implemented)
        self.alchemyStation = False
        # Upgrade 3:
        # - Unlock Forge (not implemented)
        self.forge = False
        # Upgrade 4:
        # - Egg incubator to have familiar(pets) (not implemented)
        self.eggIncubator = False
        # List with all the incubator a player has
        self.incubators: list[incubator.Incubator] = []
        # Upgrade 5:
        # - Map reader (not implemented)
        self.mapReader = False
        # Upgrade 6:
        # - Enchanting pool (not implemented)
        self.enchantingPool = False
        # Upgrade 7:
        # - not yet
        # Upgrade 8:
        # - not yet
        # Upgrade 9:
        # - not yet
        # Upgrade 10:
        # - not yet

    __max_upgrade = 10

    def upgrade_phouse(self):
        if self.upgrade <= self.__max_upgrade:
            self.upgrade += 1

        match self.upgrade:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case 6:
                pass
            case 7:
                pass
            case 8:
                pass
            case 9:
                pass
            case 10:
                pass
