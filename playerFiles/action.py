from datetime import datetime
from functions import get_timeUntilReady



class CurrentAction:
    def __init__(self, actionName: str = None, finishTime: datetime = None, itemReward: list[dict] = None, xpReward: list[tuple] = None, 
                 moneyReward: int = None, requirementReward: list[str] = None):
        '''
        Parameters
        ----------
        actionName        : String 
            The name of the action the player is doing

        finishTime        : datetime including months, days, hours, minutes, seconds
            The time at which the action is done doing. Can be None if there is no definite time

        itemReward        : List of dict of item : {'item': Item, 'nb': int}
        xpReward          : List of tuple : (number of xp (int), type of xp (string))
        moneyReward       : int 
        requirementReward : List of string 
            if the player was required to do this action at the end of it will receive the requirement.      
        '''

        self.actionName        = actionName
        self.finishTime        = finishTime
        self.itemReward        = itemReward
        self.xpReward          = xpReward
        self.moneyReward       = moneyReward
        self.requirementReward = requirementReward

    
    def reset(self):
        '''
        reset all the parameters to their default values
        '''

        self.actionName         = None
        self.finishTime         = None
        self.itemReward         = None
        self.xpReward           = None
        self.moneyReward        = None
        self.requirementReward  = None

        #TODO Save Action class in database


    def checkAction(self):
        '''
        Check if the action is over and return the time remaining if not done in string format

        Return : bool , timedelta
        '''
        remainingTime = get_timeUntilReady(readyTime=self.finishTime)
        if remainingTime == "0:00:00:000000":
            return True, "0:00:00:000000"
        return False, str(remainingTime)[:-7]
    

    def save(self):
        '''
        After each time a attribute is modified this method should be called

        save the player action in the database
        '''
        pass

    
    

