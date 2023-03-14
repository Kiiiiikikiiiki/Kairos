import items
import discord.ext.commands.context as context
from playerFiles.player import Profile

class Shop:
    def __init__(self, buying_items: list[items.Item], selling_items: list[tuple], trading_items: list[tuple]):
        self.buy = buying_items
        self.sell = selling_items
        self.trade = trading_items

        self.negociable = True  # if the player can negociate with the shop keeper 
        self.steeling = True    # If the player can steel from the shop
        self.persuasion = True  # If the player can persuade the shop keeper 


    async def interact(self, ctx: context, player: Profile):
        pass


class InteractionKairos:
    def __init__(self, description: str, subInteraction: any, requirement: any = None):
        '''
        description: Short description of the interaction to show in a dropdown
        subInteraction: The interaction type (ex: shop, talking and forge) so we can interact with the correct interaction
        requirement: A function that act like a check to know if the player can have access to this interaction
        '''
        self.desc = description
        self.subInteraction = subInteraction
        self.requirement = requirement
    

    def interact(self, ctx: context, player: Profile):
        return self.subInteraction.interact(ctx, player)


    def has_requirements(self, player: Profile):
        '''
        requirement : Function that act has a check to know if the player meet the requirement to show that interaction.

        return : True if the player meet all requirements needed. 
        '''
        return self.requirement(player)



# =======================================================
# Making the interactions list
# =======================================================
testInteract1 = InteractionKairos("Talking to tester", None)
testInteract2 = InteractionKairos("Access the shop", None)
testInteract3 = InteractionKairos("Walking to the door back store", None)
# List
testInteractions = [testInteract1, testInteract2, testInteract3]
            